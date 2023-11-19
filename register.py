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
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        rol = 'cliente'

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                sql_check_email = "SELECT id_usuario FROM Usuarios WHERE correo = %s"
                cursor.execute(sql_check_email, (correo,))
                existing_user = cursor.fetchone()

                if existing_user:
                    error_message = "El correo ya está registrado. Por favor, usa otro correo."
                else:
                    sql_insert_user = "INSERT INTO Usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)"
                    values = (nombre, correo, contrasena, rol)
                    cursor.execute(sql_insert_user, values)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    return redirect(url_for('login.login'))
            except mysql.connector.Error as err:
                print(f"Error al insertar el usuario en la base de datos: {err}")
                error_message = "Ocurrió un error al registrar el usuario. Por favor, intenta nuevamente."
        else:
            error_message = "Error de conexión a la base de datos. Por favor, intenta nuevamente."

    return render_template('register.html', error_message=error_message)
