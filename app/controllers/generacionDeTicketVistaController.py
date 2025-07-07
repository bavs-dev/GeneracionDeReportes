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
import io

generacionTicketVista_bp = Blueprint('generacionTicketVista', __name__)
dao = GeneracionTicktDAOImpl()

@generacionTicketVista_bp.route('/GeneracionTicktVista')
@login_required
def listar_tickets():
    #consulta de tickets
    prioridad = CatPrioridad.query.all()

    listTickets = Ticket.query.filter(
        Ticket.tecnico_asignado_id.is_(None)
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


    return render_template('AsignacionDeActividades/GeneracionDeTicketVista.html',listTickets=listTickets,prioridad=prioridad,solicitante=solicitante,area=area, tiposDeFalla=tiposDeFalla, estadosTicket=estadosTicket,tecnicoAsignado=tecnicoAsignado)


@generacionTicketVista_bp.route('/generacionTicketVista/actualizar_ticket/<int:id>', methods=['POST'])
@login_required
def actualizar_ticket(id):

    ticket = Ticket.query.get(id)


    if ticket:

        ticket.estado_id = request.form['estado_id']
        ticket.tecnico_asignado_id = request.form['tecnicoAsiganado']
        ticket.fecha_ultima_actualizacion =datetime.now()  # Fecha actual



        dao.actualizar(ticket)  # Asegúrate que tu DAO tenga este método
        flash('Ticket actualizado correctamente.', 'success')
    else:
        flash('Ticket no encontrado.', 'danger')

    return redirect(url_for('generacionTicketVista.listar_tickets'))


@generacionTicketVista_bp.route('/generacionTicketVista/descargar_evidencia/<int:id>')
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


