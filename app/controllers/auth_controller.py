import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario

logging.basicConfig(level=logging.INFO)

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        password = request.form['password']

        usuario = Usuario.query.filter_by(usuario=usuario_input).first()

        if usuario:
            print("Usuario encontrado:", usuario.usuario)
            print("Password válida:", usuario.check_password(password))

        if usuario and usuario.check_password(password):
            login_user(usuario)
            print("Usuario autenticado:", usuario.usuario)
            return redirect(url_for('main.dashboard_view'))
        else:
            flash('Credenciales inválidas')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # <- Cierra la sesión
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('auth.login'))