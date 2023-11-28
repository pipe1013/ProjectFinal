# actualizar.py
from flask import Blueprint, render_template
from db import connect_to_db

actualizarAdmin_routes = Blueprint('actualizarAdmin', __name__)


def obtener_admin_desde_db(id_Administrador):
    # Lógica para conectarse a la base de datos y obtener los datos del cliente
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor(dictionary=True)

        try:
            # Realiza la consulta a la base de datos
            sql = "SELECT id_Administrador, nombre_admin, apellido_admin, telefono_admin, direccion_admin FROM Administrador WHERE id_Administrador = %s"
            cursor.execute(sql, (id_Administrador,))
            administrador = cursor.fetchone()

            return administrador

        except Exception as e:
            # Maneja cualquier error que pueda ocurrir durante la consulta
            print(f"Error al obtener el cliente desde la base de datos: {str(e)}")
            return None

        finally:
            cursor.close()
            conn.close()

    return None

@actualizarAdmin_routes.route('/actualizarAdmin/<int:id_Administrador>')
def actualizarAdmin(id_Administrador):
    # Obtener el cliente de la base de datos según el ID
    administrador = obtener_admin_desde_db(id_Administrador)

    # Renderizar la plantilla y pasar el cliente como argumento
    return render_template('actualizar_administrador.html', administrador=administrador)