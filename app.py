import mysql.connector
from flask import Flask, render_template, redirect, url_for, session, request, flash
from functools import wraps
from db import connect_to_db
from authentication import login_required
from admin import admin_routes
from login import login_routes
from logout import logout_routes
from editar_horario import editar_horario_routes

from register import register_routes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'elpepe'

app.register_blueprint(admin_routes)
app.register_blueprint(login_routes)
app.register_blueprint(logout_routes)
app.register_blueprint(register_routes)
app.register_blueprint(editar_horario_routes)
if __name__ == '__main__':
    app.run(debug=True)
