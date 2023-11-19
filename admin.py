from flask import Blueprint, render_template, session, request, flash, redirect, url_for, Response
from authentication import login_required
from db import connect_to_db

admin_routes = Blueprint('admin', __name__)

def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@admin_routes.route('/admin')
@login_required
def admin():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login.login'))

    # Obtener la lista de clientes desde la base de datos (ajusta según tu implementación)
    admin = obtener_clientes_desde_db()

    return render_template('cliente.html', nombre_usuario="Nombre de usuario", clientes=admin)

@admin_routes.route('/agendar_cita')
def agendar_cita():
    # Lógica para listar clientes
    return render_template('agendar_cita.html')

@admin_routes.route('/listar_clientes')
def listar_clientes():
    # Lógica para listar clientes
    return render_template('listar_clientes.html')

@admin_routes.route('/crear_cliente', methods=['POST'])
def crear_cliente():
    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')

    # Conectar a la base de datos y ejecutar la inserción
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Insertar el nuevo cliente en la tabla Cliente
            sql_insert_cliente = "INSERT INTO Cliente (nombre, apellido, telefono, direccion) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert_cliente, (nombre, apellido, telefono, direccion))
            conn.commit()

            flash("Cliente creado exitosamente", "success")
        except Exception as e:
            flash(f"Error al crear el cliente: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

# ... (importar las bibliotecas y definir la conexión)

@admin_routes.route('/actualizar_cliente/<int:cliente_id>', methods=['POST'])
def actualizar_cliente(cliente_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')

            # Actualizar el cliente en la tabla Cliente
            sql_update_cliente = "UPDATE Cliente SET nombre = %s, apellido = %s, telefono = %s, direccion = %s WHERE id_Cliente = %s"
            cursor.execute(sql_update_cliente, (nombre, apellido, telefono, direccion, cliente_id))
            conn.commit()

            flash("Cliente actualizado exitosamente", "success")
        

        except Exception as e:
            flash(f"Error al actualizar el cliente: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))


@admin_routes.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Eliminar el cliente de la tabla Cliente
            sql_delete_cliente = "DELETE FROM Cliente WHERE id_Cliente = %s"
            cursor.execute(sql_delete_cliente, (cliente_id,))
            conn.commit()

            flash("Cliente eliminado exitosamente", "success")

        except Exception as e:
            flash(f"Error al eliminar el cliente: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

def obtener_clientes_desde_db():
    # Lógica para conectarse a la base de datos y obtener los clientes
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Realiza la consulta a la base de datos (ajusta según tu esquema)
        sql = "SELECT id_Cliente, nombre, apellido, telefono, direccion FROM Cliente"
        cursor.execute(sql)
        clientes = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convierte el resultado de la consulta en una lista de diccionarios
        columnas = ['id_Cliente', 'nombre', 'apellido', 'telefono', 'direccion']
        clientes_list = [dict(zip(columnas, cliente)) for cliente in clientes]

        return clientes_list
    
    # Retorna una lista vacía si hay algún problema con la conexión a la base de datos
    return []



