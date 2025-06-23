# archivo: create_user.py (o ejecuta en flask shell)
from app import create_app, db
from app.models.usuario import Usuario, Rol, Departamento

# Crear contexto de la app
app = create_app()
app.app_context().push()

# Verificar si el usuario ya existe
usuario_existente = Usuario.query.filter_by(usuario='admin').first()
if usuario_existente:
    print("El usuario ya existe.")
else:
    # Opcional: crear rol y departamento si no existen
    rol = Rol.query.filter_by(nombre='Administrador').first()
    if not rol:
        rol = Rol(nombre='Administrador', verificador='ok')
        db.session.add(rol)

    depto = Departamento.query.filter_by(nombre='TI').first()
    if not depto:
        depto = Departamento(nombre='TI', verificador='ok')
        db.session.add(depto)

    db.session.commit()  # Guardar rol y depto si fueron nuevos

    # Crear el nuevo usuario
    nuevo_usuario = Usuario(
        nombre='Brandon',
        apellidoP='Vasquez',
        apellidoM='Santiago',
        usuario='admin',
        correo='admin@example.com',
        departamento_id=depto.id,
        rol_id=rol.id
    )
    nuevo_usuario.set_password('123456')  # CONTRASEÑA SEGURA AQUÍ

    db.session.add(nuevo_usuario)
    db.session.commit()
    print("Usuario creado con éxito.")
