# index.py
from flask import Blueprint, render_template

cliente_routes = Blueprint('cliente', __name__)

@cliente_routes.route('/cliente')
def cliente():
    return render_template('cliente.html')

