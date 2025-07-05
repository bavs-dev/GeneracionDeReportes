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

    return redirect(url_for('generacionTicket.cargar_catalogos'))
