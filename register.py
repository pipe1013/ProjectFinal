# register.py
import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for
from db import connect_to_db

register_routes = Blueprint('register', __name__)

@register_routes.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        contrasena = request.form['contrasena']
        rol = 'administrador'

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Verificar si el nombre ya está registrado
                sql_check_nombre = "SELECT id_Administrador FROM Administrador WHERE nombre_admin = %s"
                cursor.execute(sql_check_nombre, (nombre,))
                existing_admin = cursor.fetchone()

                if existing_admin:
                    error_message = "El nombre ya está registrado. Por favor, usa otro nombre."
                else:
                    # Insertar nuevo administrador
                    sql_insert_admin = "INSERT INTO Administrador (nombre_admin, apellido_admin, telefono_admin, direccion_admin, contrasena) VALUES (%s, %s, %s, %s, %s)"
                    values = (nombre, apellido, telefono, direccion, contrasena)
                    cursor.execute(sql_insert_admin, values)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    return redirect(url_for('login.login'))
            except mysql.connector.Error as err:
                print(f"Error al insertar el administrador en la base de datos: {err}")
                error_message = "Ocurrió un error al registrar el administrador. Por favor, intenta nuevamente."
        else:
            error_message = "Error de conexión a la base de datos. Por favor, intenta nuevamente."

    return render_template('register.html', error_message=error_message)
