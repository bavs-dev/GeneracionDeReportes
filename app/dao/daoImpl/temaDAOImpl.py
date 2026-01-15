# app/dao/impl/tema_soporte_dao_impl.py CatTemaSoporte
from app.models.catalogos_models import TiposFalla
from app import db
from app.dao.temaDAO import TemaSoporteDAO

class TemaSoporteDAOImpl(TemaSoporteDAO):

    def obtener_todos(self, page=1, per_page=5):
        return TiposFalla.query.order_by(TiposFalla.id).paginate(page=page, per_page=per_page)

    def obtener_por_id(self, id):
        return TiposFalla.query.get(id)

    def guardar(self, nombre):
        verificador = nombre.replace(" ", "").upper()
        tema = TiposFalla(nombre=nombre, verificador=verificador)
        db.session.add(tema)
        db.session.commit()

    def actualizar(self, id, nombre):
        tema = TiposFalla.query.get(id)
        if tema:
            tema.nombre = nombre
            tema.verificador = nombre.replace(" ", "").upper()
            db.session.commit()

    def eliminar(self, id):
        tema = TiposFalla.query.get(id)
        if tema:
            db.session.delete(tema)
            db.session.commit()
