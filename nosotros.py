# index.py
from flask import Blueprint, render_template

nosotros_routes = Blueprint('nosotros', __name__)

@nosotros_routes.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')
