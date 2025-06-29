from app.models.usuario import Usuario, db
from app.dao.usuario_dao import UsuarioDAO

class UsuarioDAOImpl(UsuarioDAO):

    def obtener_todos(self):
        return Usuario.query.all()

    def obtener_por_id(self, id):
        return Usuario.query.get(id)

    def crear(self, usuario):
        db.session.add(usuario)
        db.session.commit()

    def actualizar(self, usuario):
        db.session.commit()

    def eliminar(self, id):
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
