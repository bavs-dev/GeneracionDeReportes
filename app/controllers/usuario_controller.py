from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.dao.daoImpl.usuario_dao_impl import UsuarioDAOImpl
from app.models.usuario import Usuario, Departamento, Rol
from flask_login import login_user, logout_user, login_required, current_user
usuario_bp = Blueprint('usuarios', __name__)
dao = UsuarioDAOImpl()


@usuario_bp.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = dao.obtener_todos()
    departamentos = Departamento.query.all()
    roles = Rol.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios, departamentos=departamentos, roles=roles)


@usuario_bp.route('/usuarios/crear', methods=['POST'])
@login_required
def crear_usuario():
    nuevo_usuario = Usuario(
        nombre=request.form['nombre'],
        apellidoP=request.form['apellidoP'],
        apellidoM=request.form['apellidoM'],
        usuario=request.form['usuario'],
        correo=request.form['correo'],
        departamento_id=request.form['departamento_id'],
        rol_id=request.form['rol_id']
    )
    nuevo_usuario.set_password(request.form['password'])
    dao.crear(nuevo_usuario)
    flash('Usuario creado exitosamente', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))


@usuario_bp.route('/usuarios/editar/<int:id>', methods=['POST'])
@login_required
def editar_usuario(id):
    usuario = dao.obtener_por_id(id)
    if usuario:
        usuario.nombre = request.form['nombre']
        usuario.apellidoP = request.form['apellidoP']
        usuario.apellidoM = request.form['apellidoM']
        usuario.usuario = request.form['usuario']
        usuario.correo = request.form['correo']
        usuario.departamento_id = request.form['departamento_id']
        usuario.rol_id = request.form['rol_id']

        if request.form['password']:
            usuario.set_password(request.form['password'])

        dao.actualizar(usuario)
        flash('Usuario actualizado correctamente', 'success')

    return redirect(url_for('usuarios.listar_usuarios'))


@usuario_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    dao.eliminar(id)
    flash('Usuario eliminado', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))
