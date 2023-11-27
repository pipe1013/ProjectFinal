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

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Verificar si el nombre ya está registrado
                sql_check_nombre = "SELECT id_Cliente FROM Cliente WHERE nombre = %s"
                cursor.execute(sql_check_nombre, (nombre,))
                existing_cliente = cursor.fetchone()

                if existing_cliente:
                    error_message = "El nombre ya está registrado. Por favor, usa otro nombre."
                else:
                    # Insertar nuevo cliente
                    sql_insert_cliente = "INSERT INTO Cliente (nombre, apellido, telefono, direccion, contrasena) VALUES (%s, %s, %s, %s, %s)"
                    values = (nombre, apellido, telefono, direccion, contrasena)
                    cursor.execute(sql_insert_cliente, values)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    return redirect(url_for('login.login'))
            except mysql.connector.Error as err:
                print(f"Error al insertar el cliente en la base de datos: {err}")
                error_message = "Ocurrió un error al registrar el cliente. Por favor, intenta nuevamente."
        else:
            error_message = "Error de conexión a la base de datos. Por favor, intenta nuevamente."

    return render_template('register.html', error_message=error_message)
