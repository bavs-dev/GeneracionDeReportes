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
from flask import send_file, make_response
from flask_login import current_user


import io

reporteTicket_bp = Blueprint('reporteTicket', __name__)
dao = GeneracionTicktDAOImpl()

@reporteTicket_bp.route('/reporteTicket')
@login_required
def listar_tickets():
    #consulta de tickets
    prioridad = CatPrioridad.query.all()
    usuario_id = current_user.id

    listTickets = Ticket.query.filter(
        Ticket.solicitante_id == current_user.id,
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


@reporteTicket_bp.route('/reporteTicket/actualizar_ticket/<int:id>', methods=['POST'])
@login_required
def actualizar_ticket(id):

    ticket = Ticket.query.get(id)


    if ticket:
        ticket.cat_prioridad = request.form['cat_prioridad']
        ticket.asunto = request.form['asunto']
        ticket.solicitante_id = request.form['solicitante_id']
        ticket.afectado_id = request.form['afectado_id']
        ticket.tema_soporte = request.form['tema_soporte']
        ticket.area = request.form['area']
        ticket.tipo_falla_id = request.form['tipo_falla_id']
        ticket.service_tag = request.form['service_tag']
        ticket.numero_serie = request.form['numero_serie']
        ticket.ip_equipo = request.form['ip_equipo']
        ticket.descripcion_equipo = request.form['descripcion_equipo']
        ticket.extension = request.form['extension']
        ticket.piso = request.form['piso']
        ticket.datos_atencion = request.form['datos_atencion']
        ticket.comentario_usuario = request.form['comentario_usuario']
        ticket.sugerencias = request.form['sugerencias']
        ticket.estado_id = request.form['estado_id']
        ticket.tecnico_asignado_id = request.form['tecnicoAsiganado']

        # Si subió evidencia nueva:
        if 'evidencia' in request.files and request.files['evidencia']:
            evidencia = request.files['evidencia'].read()
            ticket.evidencia = evidencia

        dao.actualizar(ticket)  # Asegúrate que tu DAO tenga este método
        flash('Ticket actualizado correctamente.', 'success')
    else:
        flash('Ticket no encontrado.', 'danger')

    return redirect(url_for('generacionTicketVista.listar_tickets'))


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


