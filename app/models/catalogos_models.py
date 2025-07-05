from app import db

class CatCalidad(db.Model):
    __tablename__ = 'cat_calidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    verificador = db.Column(db.String(50), nullable=False)


class CatPrioridad(db.Model):
    __tablename__ = 'cat_prioridad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    verificador = db.Column(db.String(50), nullable=False)


class CatTemaSoporte(db.Model):
    __tablename__ = 'cat_tema_soporte'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    verificador = db.Column(db.String(50), nullable=False)


class EstadosTicket(db.Model):
    __tablename__ = 'estados_ticket'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    verificador = db.Column(db.String(50), nullable=False)


class TiposFalla(db.Model):
    __tablename__ = 'tipos_falla'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    verificador = db.Column(db.String(50), nullable=False)

class cat_area(db.Model):
    __tablename__ = 'cat_area'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    verificador = db.Column(db.String(50), nullable=False)
