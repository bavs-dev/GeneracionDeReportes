# app/dao/impl/area_dao_impl.py
from app.models.catalogos_models import cat_area
from app import db
from app.dao.areaDAO import AreaDAO

class AreaDAOImpl(AreaDAO):

    def obtener_todos(self, page=1, per_page=5):
        return cat_area.query.order_by(cat_area.id).paginate(page=page, per_page=per_page)

    def obtener_por_id(self, id):
        return cat_area.query.get(id)

    def guardar(self, nombre):
        verificador = nombre.replace(" ", "").upper()
        area = cat_area(nombre=nombre, verificador=verificador)
        db.session.add(area)
        db.session.commit()

    def actualizar(self, id, nombre):
        area = cat_area.query.get(id)
        if area:
            area.nombre = nombre
            area.verificador = nombre.replace(" ", "").upper()
            db.session.commit()

    def eliminar(self, id):
        area = cat_area.query.get(id)
        if area:
            db.session.delete(area)
            db.session.commit()
