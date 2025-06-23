from flask import Blueprint, render_template, make_response
from flask_login import login_required, current_user

main = Blueprint('main', __name__)  # Este nombre lo usas en url_for('main.algo')

@main.route('/dashboard')
@login_required
def dashboard_view():
    response = make_response(render_template('dashboard.html', usuario=current_user))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


