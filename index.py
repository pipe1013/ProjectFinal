# index.py
from flask import Blueprint, render_template, session, redirect, url_for

index_routes = Blueprint('index', __name__)

@index_routes.route('/')
def index():
    return render_template('index.html')

@index_routes.route('/logout', methods=['GET'])
def logout():
    # Limpiar la sesión al cerrar sesión
    session.clear()
    return redirect(url_for('index.index'))