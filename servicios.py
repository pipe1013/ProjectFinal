# index.py
from flask import Blueprint, render_template

servicios_routes = Blueprint('servicios', __name__)

@servicios_routes.route('/servicios')
def servicios():
    return render_template('servicios.html')
