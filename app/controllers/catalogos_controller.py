# controllers/catalogos_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.dao.daoImpl.temaDAOImpl import TemaSoporteDAOImpl
from app.dao.daoImpl.areaDAOImpl import AreaDAOImpl

catalogos_bp = Blueprint('catalogos', __name__)
tema_dao = TemaSoporteDAOImpl()
area_dao = AreaDAOImpl()

# ---------- Temas ----------
@catalogos_bp.route('/catalogos/temas', methods=['GET'])
def vista_temas():
    page = request.args.get('page', 1, type=int)
    temas = tema_dao.obtener_todos(page)
    return render_template('catalogos/temas.html', temas=temas)

@catalogos_bp.route('/catalogos/tema/agregar', methods=['POST'])
def agregar_tema():
    nombre = request.form['nombre']
    id = request.form.get('id')
    if id:
        tema_dao.actualizar(id, nombre)
        flash('Tema actualizado correctamente.', 'success')
    else:
        tema_dao.guardar(nombre)
        flash('Tema agregado correctamente.', 'success')
    return redirect(url_for('catalogos.vista_temas'))

@catalogos_bp.route('/catalogos/tema/eliminar/<int:id>', methods=['POST'])
def eliminar_tema(id):
    tema_dao.eliminar(id)
    flash('Tema eliminado correctamente.', 'success')
    return redirect(url_for('catalogos.vista_temas'))

# ---------- Áreas ----------
@catalogos_bp.route('/catalogos/areas', methods=['GET'])
def vista_areas():
    page = request.args.get('page', 1, type=int)
    areas = area_dao.obtener_todos(page)
    return render_template('catalogos/areas.html', areas=areas)

@catalogos_bp.route('/catalogos/area/agregar', methods=['POST'])
def agregar_area():
    nombre = request.form['nombre']
    id = request.form.get('id')
    if id:
        area_dao.actualizar(id, nombre)
        flash('Área actualizada correctamente.', 'success')
    else:
        area_dao.guardar(nombre)
        flash('Área agregada correctamente.', 'success')
    return redirect(url_for('catalogos.vista_areas'))

@catalogos_bp.route('/catalogos/area/eliminar/<int:id>', methods=['POST'])
def eliminar_area(id):
    area_dao.eliminar(id)
    flash('Área eliminada correctamente.', 'success')
    return redirect(url_for('catalogos.vista_areas'))
