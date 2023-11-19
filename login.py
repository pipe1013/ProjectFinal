# login.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from db import connect_to_db

login_routes = Blueprint('login', __name__)

@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT id_Administrador, nombre_admin, apellido_admin, telefono_admin, direccion_admin, contrasena FROM Administrador WHERE nombre_admin = %s AND contrasena = %s LIMIT 1"
            values = (nombre, contrasena)
            cursor.execute(sql, values)
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['user_role'] = 'admin'  # Asignar un rol específico para los clientes

                return redirect(url_for('admin.admin'))
            else:
                error_message = "Credenciales inválidas. Por favor, intenta nuevamente."

    return render_template('login.html', error_message=error_message)
