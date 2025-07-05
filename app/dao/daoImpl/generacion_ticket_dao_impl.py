from app.models.ticket_models import Ticket,db
from app.dao.generacion_ticket_dao import GeneracionTicktDAO

class GeneracionTicktDAOImpl(GeneracionTicktDAO):

    def obtener_todos(self):
        return Ticket.query.all()

    def obtener_por_id(self, id):
        return Ticket.query.get(id)

    def crear(self, Ticket):
        db.session.add(Ticket)
        db.session.commit()

    def actualizar(self, Ticket):
        db.session.commit()

    def eliminar(self, id):
        ticket = Ticket.query.get(id)
        if ticket:
            db.session.delete(ticket)
            db.session.commit()