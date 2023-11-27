# actualizar.py
from flask import Blueprint, render_template
from db import connect_to_db

actualizar_routes = Blueprint('actualizar', __name__)


def obtener_cliente_desde_db(cliente_id):
    # Lógica para conectarse a la base de datos y obtener los datos del cliente
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor(dictionary=True)

        try:
            # Realiza la consulta a la base de datos
            sql = "SELECT id_Cliente, nombre, apellido, telefono, direccion FROM Cliente WHERE id_Cliente = %s"
            cursor.execute(sql, (cliente_id,))
            cliente = cursor.fetchone()

            return cliente

        except Exception as e:
            # Maneja cualquier error que pueda ocurrir durante la consulta
            print(f"Error al obtener el cliente desde la base de datos: {str(e)}")
            return None

        finally:
            cursor.close()
            conn.close()

    return None

@actualizar_routes.route('/actualizar/<int:cliente_id>')
def actualizar(cliente_id):
    # Obtener el cliente de la base de datos según el ID
    cliente = obtener_cliente_desde_db(cliente_id)

    # Renderizar la plantilla y pasar el cliente como argumento
    return render_template('actualizar_cliente.html', cliente=cliente)
