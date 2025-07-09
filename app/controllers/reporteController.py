from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.dao.daoImpl.generacion_ticket_dao_impl import  GeneracionTicktDAOImpl
from app.models.ticket_models import  Ticket,ComentarioTicket,HistorialEstadosTicket
from app.models.usuario import  Usuario
from app.models.catalogos_models import  EstadosTicket,CatCalidad,CatPrioridad,CatTemaSoporte,TiposFalla,cat_area,Piso
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from app.models import Ticket  # Ajusta según tu estructura
from sqlalchemy import func
from flask import send_file, make_response
import io
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import datetime
from reportlab.pdfgen import canvas
from app import db  # <-- Ajusta si está en otro módulo o carpeta
from flask_login import current_user



reporteTicket_bp = Blueprint('reporteTicket', __name__)
dao = GeneracionTicktDAOImpl()

@reporteTicket_bp.route('/reporteTicket')
@login_required
def listar_tickets():
    #consulta de tickets
    prioridad = CatPrioridad.query.all()
    usuario_id = current_user.id

    # Suponiendo que el id del rol se guarda así
    if current_user.rol_id == 3:
        # Solo ver tickets asignados a él
        listTickets = Ticket.query.filter(
            Ticket.tecnico_asignado_id == current_user.id
        ).all()
    else:
        # Ver todos los tickets que tienen técnico asignado
        listTickets = Ticket.query.filter(
            Ticket.tecnico_asignado_id.isnot(None)
        ).all()

    solicitante = Usuario.query.filter(
        or_(
            Usuario.rol_id == 1,
            Usuario.rol_id == 2
        )
    ).all()

    area = cat_area.query.all()

    tiposDeFalla = TiposFalla.query.all()

    estadosTicket = EstadosTicket.query.all()
    tecnicoAsignado =  Usuario.query.filter(
        (
            Usuario.rol_id == 3
        )
    ).all()



    return render_template('Reportes/ReportesDeticketVista.html',listTickets=listTickets,prioridad=prioridad,solicitante=solicitante,area=area, tiposDeFalla=tiposDeFalla, estadosTicket=estadosTicket,tecnicoAsignado=tecnicoAsignado,
    current_user=current_user)

def generar_numero_ticket():
    hoy = datetime.now().strftime('%Y%m%d')  # Ejemplo: 20240705
    prefijo = f"T-{hoy}-"

    # Contar cuántos tickets existen hoy para incrementar el consecutivo
    conteo = Ticket.query.filter(Ticket.numero_ticket.like(f"{prefijo}%")).count()
    nuevo_numero = f"{prefijo}{conteo + 1}"

    return nuevo_numero

@reporteTicket_bp.route('/reporteTicket/actualizar_ticket/<int:id>', methods=['POST'])
@login_required
def actualizar_ticket(id):
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    import pandas as pd

    ticket = Ticket.query.get(id)

    if not ticket:
        flash('Ticket no encontrado.', 'danger')
        return redirect(url_for('reporteTicket.listar_tickets'))

    # Actualiza el estado
    nuevo_estado_id = request.form.get('estado_id')
    if nuevo_estado_id:
        ticket.estado_id = int(nuevo_estado_id)
        dao.actualizar(ticket)
    else:
        flash('Estado no proporcionado.', 'warning')
        return redirect(url_for('reporteTicket.listar_tickets'))

    # Consultas necesarias para el PDF
    prioridad = db.session.query(CatPrioridad).filter_by(id=ticket.cat_prioridad).first()
    tipo_falla = db.session.query(TiposFalla).filter_by(id=ticket.tipo_falla_id).first()
    piso = db.session.query(Piso).filter_by(id=ticket.piso).first()
    area = db.session.query(cat_area).filter_by(id=ticket.area).first()
    estadosTicket = db.session.query(EstadosTicket).filter_by(id=ticket.estado_id).first()
    flash('Ticket creado exitosamente', 'success')
    carpeta = os.path.join('static', 'tickets')
    os.makedirs(carpeta, exist_ok=True)

    ruta_pdf = os.path.join(carpeta, f'Ticket_{ticket.numero_ticket}.pdf')
    ruta_excel = os.path.join(carpeta, f'Ticket_{ticket.numero_ticket}.xlsx')

    # Generar PDF tipo ticket
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas

    p = canvas.Canvas(ruta_pdf, pagesize=(100 * mm, 300 * mm))  # Ticket de 80mm ancho x 300mm alto
    p.setFont("Helvetica", 9)

    y = 280 * mm  # Altura inicial
    line_height = 5 * mm

    # Campos con la información completa
    campos = {
        "Número Ticket": ticket.numero_ticket,
        "Estado Ticket": estadosTicket.nombre,
        "Asunto": ticket.asunto,
        "Prioridad": prioridad.nombre if prioridad else "Desconocido",
        "Solicitante": ticket.solicitante_id,
        "Afectado": ticket.afectado_id,
        "Área": area.nombre,
        "Tipo de Falla": tipo_falla.nombre if tipo_falla else "Desconocido",
        "Service Tag": ticket.service_tag,
        "Número de Serie": ticket.numero_serie,
        "IP del Equipo": ticket.ip_equipo,
        "Extensión": ticket.extension,
        "Piso": piso.nombre if piso else "Desconocido",
        "Datos de Atención": ticket.datos_atencion,
        "Comentario del Usuario": ticket.comentario_usuario,
        "Sugerencias": ticket.sugerencias,
        "Fecha de Registro": ticket.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
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
    pdf_url = url_for('static', filename=f'tickets/Ticket_{ticket.numero_ticket}.pdf')
    excel_url = url_for('static', filename=f'tickets/Ticket_{ticket.numero_ticket}.xlsx')

    # Imprimir rutas en consola
    print("Ruta absoluta PDF:", os.path.abspath(ruta_pdf))
    print("Ruta absoluta Excel:", os.path.abspath(ruta_excel))
    print("URL PDF:", pdf_url)
    print("URL Excel:", excel_url)

    return jsonify({'success': True, 'pdf_url': pdf_url, 'excel_url': excel_url})


@reporteTicket_bp.route('/reporteTicket/descargar_evidencia/<int:id>')
@login_required
def descargar_evidencia(id):
    ticket = Ticket.query.get(id)
    if not ticket or not ticket.evidencia:
        return "Archivo no encontrado", 404

    return send_file(
        io.BytesIO(ticket.evidencia),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=f"evidencia_ticket_{id}.pdf"
    )



@reporteTicket_bp.route('/reporteTicket/descargar_evidencias/<int:id>')
@login_required
def descargar_evidencias(id):
    ticket = Ticket.query.get(id)
    if not ticket or not ticket.evidencia:
        return "Archivo no encontrado", 404

    return send_file(
        io.BytesIO(ticket.evidencia),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=f"evidencia_ticket_{id}.pdf"
    )
