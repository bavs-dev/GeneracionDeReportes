from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.dao.daoImpl.generacion_ticket_dao_impl import  GeneracionTicktDAOImpl
from app.models.ticket_models import  Ticket,ComentarioTicket,HistorialEstadosTicket
from app.models.usuario import  Usuario
from app.models.catalogos_models import  EstadosTicket,CatCalidad,CatPrioridad,CatTemaSoporte,TiposFalla,cat_area
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from app.models import Ticket  # Ajusta según tu estructura
from sqlalchemy import func
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
import pandas as pd
generacionTicket_bp = Blueprint('generacionTicket', __name__)
dao = GeneracionTicktDAOImpl()


#creacion del metodo de cargar furmlario

@generacionTicket_bp.route('/generacionTicket')
@login_required # colocamos el logeo necesario
def cargar_catalogos():
    prioridad = CatPrioridad.query.all()
    #consulta para traer los afectados

    solicitante = Usuario.query.filter(
        or_(
            Usuario.rol_id == 1,
            Usuario.rol_id == 2
        )
    ).all()

    area = cat_area.query.all()

    tiposDeFalla = TiposFalla.query.all()

    return render_template('Ticket/GeneracionDeTicket.html', prioridad=prioridad, solicitante=solicitante,area=area,tiposDeFalla=tiposDeFalla)

def generar_numero_ticket():
    hoy = datetime.now().strftime('%Y%m%d')  # Ejemplo: 20240705
    prefijo = f"T-{hoy}-"

    # Contar cuántos tickets existen hoy para incrementar el consecutivo
    conteo = Ticket.query.filter(Ticket.numero_ticket.like(f"{prefijo}%")).count()
    nuevo_numero = f"{prefijo}{conteo + 1}"

    return nuevo_numero

@generacionTicket_bp.route('/generacionTicket/levantar_ticket', methods=['POST'])
@login_required
def crear_reporte():
    evidencia_file = request.files['evidencia']

    if evidencia_file and evidencia_file.filename != '':
        evidencia_data = evidencia_file.read()
    else:
        evidencia_data = None
    numero_ticket_generado = generar_numero_ticket()
    nuevo_tiket = Ticket(
        numero_ticket=numero_ticket_generado,
        cat_prioridad=int(request.form['cat_prioridad']),
        asunto=request.form['asunto'],
        solicitante_id=int(request.form['solicitante_id']),
        afectado_id=int(request.form['afectado_id']),
        tema_soporte=request.form['tema_soporte'],
        area=int(request.form['area']),
        tipo_falla_id=int(request.form['tipo_falla_id']),
        service_tag=request.form['service_tag'],
        numero_serie=request.form['numero_serie'],
        ip_equipo=request.form['ip_equipo'],
        descripcion_equipo=request.form['descripcion_equipo'],
        extension=request.form['extension'],
        piso=request.form['piso'],
        datos_atencion=request.form['datos_atencion'],
        comentario_usuario=request.form['comentario_usuario'],
        sugerencias=request.form['sugerencias'],
        evidencia=evidencia_data,
        fecha_registro=datetime.now()  # Fecha actual
    )

    dao.crear(nuevo_tiket)

    flash('Ticket creado exitosamente', 'success')
    carpeta = os.path.join('static', 'tickets')
    os.makedirs(carpeta, exist_ok=True)

    ruta_pdf = os.path.join(carpeta, f'Ticket_{numero_ticket_generado}.pdf')
    ruta_excel = os.path.join(carpeta, f'Ticket_{numero_ticket_generado}.xlsx')

    # Generar PDF tipo ticket
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas

    p = canvas.Canvas(ruta_pdf, pagesize=(80 * mm, 300 * mm))  # Ticket de 80mm ancho x 300mm alto
    p.setFont("Helvetica", 9)

    y = 280 * mm  # Altura inicial
    line_height = 5 * mm

    # Campos con la información completa
    campos = {
        "Número Ticket": nuevo_tiket.numero_ticket,
        "Asunto": nuevo_tiket.asunto,
        "Prioridad": nuevo_tiket.cat_prioridad,
        "Solicitante ID": nuevo_tiket.solicitante_id,
        "Afectado ID": nuevo_tiket.afectado_id,
        "Tema de Soporte": nuevo_tiket.tema_soporte,
        "Área": nuevo_tiket.area,
        "Tipo de Falla": nuevo_tiket.tipo_falla_id,
        "Service Tag": nuevo_tiket.service_tag,
        "Número de Serie": nuevo_tiket.numero_serie,
        "IP del Equipo": nuevo_tiket.ip_equipo,
        "Descripción del Equipo": nuevo_tiket.descripcion_equipo,
        "Extensión": nuevo_tiket.extension,
        "Piso": nuevo_tiket.piso,
        "Datos de Atención": nuevo_tiket.datos_atencion,
        "Comentario del Usuario": nuevo_tiket.comentario_usuario,
        "Sugerencias": nuevo_tiket.sugerencias,
        "Fecha de Registro": nuevo_tiket.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Título del ticket
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(40 * mm, y, "📌 TICKET DE SOPORTE")
    y -= 10 * mm
    p.line(5 * mm, y, 75 * mm, y)
    y -= line_height

    p.setFont("Helvetica", 9)

    # Contenido del ticket
    for campo, valor in campos.items():
        texto = f"{campo}: {valor}"
        p.drawString(5 * mm, y, texto)
        y -= line_height
        if y < 20 * mm:
            p.showPage()
            y = 280 * mm
            p.setFont("Helvetica", 9)

    # Línea final
    p.line(5 * mm, y, 75 * mm, y)
    y -= line_height
    p.drawCentredString(40 * mm, y, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    p.showPage()
    p.save()

    # Generar Excel detallado
    import pandas as pd
    data_excel = {k: [v] for k, v in campos.items()}
    df = pd.DataFrame(data_excel)
    df.to_excel(ruta_excel, index=False)

    # URLs para descargar
    pdf_url = url_for('static', filename=f'tickets/Ticket_{numero_ticket_generado}.pdf')
    excel_url = url_for('static', filename=f'tickets/Ticket_{numero_ticket_generado}.xlsx')

    # Imprimir rutas en consola
    print("Ruta absoluta PDF:", os.path.abspath(ruta_pdf))
    print("Ruta absoluta Excel:", os.path.abspath(ruta_excel))
    print("URL PDF:", pdf_url)
    print("URL Excel:", excel_url)

    return jsonify({'success': True, 'pdf_url': pdf_url, 'excel_url': excel_url})
