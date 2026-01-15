from sqlalchemy.orm import backref

from app import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    numero_ticket = db.Column(db.String(50), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    cat_prioridad = db.Column(db.Integer, db.ForeignKey('cat_prioridad.id'), nullable=False)
    asunto = db.Column(db.String(255), nullable=False)

    solicitante_id  = db.Column(db.String(255), nullable=False)
    afectado_id  = db.Column(db.String(255), nullable=False)
    tecnico_asignado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)



    area = db.Column(db.Integer, db.ForeignKey('cat_area.id'), nullable=True)

    extension = db.Column(db.String(50))
    piso = db.Column(db.Integer, db.ForeignKey('piso.id'), nullable=True)
    piso = db.Column(db.Integer, db.ForeignKey('piso.id'), nullable=False)



    datos_atencion = db.Column(db.Text)
    comentario_usuario = db.Column(db.Text)
    sugerencias = db.Column(db.Text)

    tipo_falla_id = db.Column(db.Integer, db.ForeignKey('tipos_falla.id'), nullable=False)
    service_tag = db.Column(db.String(100))
    numero_serie = db.Column(db.String(100))
    ip_equipo = db.Column(db.String(100))


    evidencia = db.Column(db.LargeBinary, nullable=True)

    fecha_solucion = db.Column(db.DateTime, nullable=True)
    fecha_ultima_actualizacion = db.Column(db.DateTime, nullable=True)

    estado_id = db.Column(db.Integer, db.ForeignKey('estados_ticket.id'), nullable=False, default=1)
    cat_calidad_id = db.Column(db.Integer, db.ForeignKey('cat_calidad.id'), nullable=True)
    # Relación hacia la tabla CatPrioridad
    prioridad = db.relationship('CatPrioridad', backref='tickets')
    estadosTicketid = db.relationship('EstadosTicket', foreign_keys=[estado_id])
    piso_rel = db.relationship('Piso', backref='tickets')

    tecnico_asignado = db.relationship('Usuario', foreign_keys=[tecnico_asignado_id])


class ComentarioTicket(db.Model):
    __tablename__ = 'comentarios_ticket'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha_comentario = db.Column(db.DateTime, default=datetime.utcnow)
    evidencia = db.Column(db.LargeBinary, nullable=True)


class HistorialEstadosTicket(db.Model):
    __tablename__ = 'historial_estados_ticket'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados_ticket.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
