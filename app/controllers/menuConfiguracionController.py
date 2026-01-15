from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.dao.daoImpl.generacion_ticket_dao_impl import  GeneracionTicktDAOImpl
from app.models.ticket_models import  Ticket,ComentarioTicket,HistorialEstadosTicket
from app.models.usuario import  Usuario
from app.models.catalogos_models import  EstadosTicket,CatCalidad,CatPrioridad,CatTemaSoporte,TiposFalla,cat_area,Piso
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from app.models import Ticket  # Ajusta según tu estructura
from sqlalchemy import func
from flask import send_file, make_response
import io
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import datetime
from reportlab.pdfgen import canvas
from app import db  # <-- Ajusta si está en otro módulo o carpeta
from flask_login import current_user


menu_configuracion_bp = Blueprint('menu_configuracion', __name__)
dao = GeneracionTicktDAOImpl()
@menu_configuracion_bp.route('/menu_configuracion')
@login_required
def menu_configuracion():
    return render_template('Configuracion/menu_configuracion.html')
