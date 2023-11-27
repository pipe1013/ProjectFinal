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

            # Buscar en la tabla Administrador
            sql_admin = "SELECT id_Administrador, nombre_admin, contrasena FROM Administrador WHERE nombre_admin = %s AND contrasena = %s LIMIT 1"
            cursor.execute(sql_admin, (nombre, contrasena))
            admin = cursor.fetchone()

            # Buscar en la tabla Cliente
            sql_cliente = "SELECT id_Cliente, nombre, contrasena FROM Cliente WHERE nombre = %s AND contrasena = %s LIMIT 1"
            cursor.execute(sql_cliente, (nombre, contrasena))
            cliente = cursor.fetchone()

            cursor.close()
            conn.close()

            if admin:
                # Si es administrador, asignar sesión y redirigir a la ruta de administrador
                session['user_id'] = admin[0]
                session['user_name'] = admin[1]
                session['user_role'] = 'admin'
                return redirect(url_for('admin.admin'))
            elif cliente:
                # Si es cliente, asignar sesión y redirigir a la ruta de cliente
                session['user_id'] = cliente[0]
                session['user_name'] = cliente[1]
                session['user_role'] = 'cliente'
                return redirect(url_for('cliente.cliente'))
            else:
                error_message = "Credenciales inválidas. Por favor, intenta nuevamente."

    return render_template('login.html', error_message=error_message)
