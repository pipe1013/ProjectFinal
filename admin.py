from flask import Blueprint, render_template, session, request, flash, redirect, url_for, Response
from authentication import login_required
from db import connect_to_db
import mysql.connector

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

    return render_template('admin.html', nombre_usuario="Nombre de usuario", clientes=admin)

@admin_routes.route('/crearAdmin')
def crearAdmin():
    datos_administradores = obtener_administradores_desde_db()

    # Renderiza la plantilla y pasa los datos como argumento
    return render_template('crearAdmin.html', nombre_usuario="Nombre de usuario", datos_administradores=datos_administradores)

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

@admin_routes.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    error_message = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        contrasena = request.form['contrasena']
        rol = 'administrador'

        # Agrega esta impresión para verificar los datos
        print(f"Datos del nuevo administrador: {nombre}, {apellido}, {telefono}, {direccion}, {contrasena}")

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

                    return redirect(url_for('admin.crearAdmin'))
            except mysql.connector.Error as err:
                print(f"Error al insertar el administrador en la base de datos: {err}")
                error_message = "Ocurrió un error al registrar el administrador. Por favor, intenta nuevamente."
        else:
            error_message = "Error de conexión a la base de datos. Por favor, intenta nuevamente."

    return render_template('crearAdmin.html', error_message=error_message)


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

from flask import render_template  # Asegúrate de importar render_template

@admin_routes.route('/actualizar_administrador/<int:admin_id>', methods=['POST'])
def actualizar_administrador(admin_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')

            # Actualizar el administrador en la tabla Administrador
            sql_update_admin = "UPDATE Administrador SET nombre_admin = %s, apellido_admin = %s, telefono_admin = %s, direccion_admin = %s WHERE id_Administrador = %s"
            cursor.execute(sql_update_admin, (nombre, apellido, telefono, direccion, admin_id))
            conn.commit()

            flash("Administrador actualizado exitosamente", "success")

        except Exception as e:
            flash(f"Error al actualizar el administrador: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('admin.crearAdmin'))


@admin_routes.route('/eliminar_administrador/<int:admin_id>', methods=['POST'])
def eliminar_administrador(admin_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Eliminar el administrador de la tabla Administrador
            sql_delete_admin = "DELETE FROM Administrador WHERE id_Administrador = %s"
            cursor.execute(sql_delete_admin, (admin_id,))
            conn.commit()

            flash("Administrador eliminado exitosamente", "success")

        except Exception as e:
            flash(f"Error al eliminar el administrador: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('admin.crearAdmin'))

@admin_routes.route('/gestionar_clientes')
@login_required
def gestionar_clientes():
    # Obtén los datos desde la base de datos
    datos_clientes = connect_to_db()

    # Renderiza la plantilla y pasa los datos como argumento
    return render_template('admin.html', nombre_usuario="Nombre de usuario", datos_clientes=datos_clientes)

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

@admin_routes.route('/gestionar_administradores')
@login_required
def gestionar_administradores():
    # Obtén los datos desde la base de datos
    datos_administradores = obtener_administradores_desde_db()

    # Renderiza la plantilla y pasa los datos como argumento
    return render_template('crearAdmin.html', nombre_usuario="Nombre de usuario", datos_administradores=datos_administradores)

def obtener_administradores_desde_db():
    # Lógica para conectarse a la base de datos y obtener los administradores
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Realiza la consulta a la base de datos (ajusta según tu esquema)
        sql = "SELECT id_Administrador, nombre_admin, apellido_admin, telefono_admin, direccion_admin FROM Administrador"
        cursor.execute(sql)
        administradores = cursor.fetchall()
        print (administradores) 
        cursor.close()
        conn.close()
        # Convierte el resultado de la consulta en una lista de diccionarios
        columnas = ['id_Administrador', 'nombre_admin', 'apellido_admin', 'telefono_admin', 'direccion_admin']
        administradores_list = [dict(zip(columnas, admin)) for admin in administradores]

        return administradores_list
    
    
    # Retorna una lista vacía si hay algún problema con la conexión a la base de datos
    return []

@admin_routes.route('/adminPedidos')
@login_required
def adminPedidos():
    # Obtén los datos de los servicios desde la base de datos
    servicios = obtener_servicios_desde_db()

    # Renderiza la plantilla y pasa los datos como argumento
    return render_template('adminPedidos.html', nombre_usuario="Nombre de usuario", servicios=servicios)

def obtener_servicios_desde_db():
    # Lógica para conectarse a la base de datos y obtener los servicios agendados
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        sql = "SELECT id_Servicio, fecha_recogida, cantidad, Tipo_de_Servicio.nombre AS tipo_servicio, prenda.nombre AS tipo_prenda, cliente.nombre AS nombre_cliente, cliente.apellido AS apellido_cliente FROM Servicio " \
      "JOIN Tipo_de_Servicio ON Servicio.id_TipoServicio = Tipo_de_Servicio.id_TipoServicio " \
      "JOIN Tipo_de_Prenda AS prenda ON Servicio.id_Prenda = prenda.id_Prenda " \
      "JOIN Cliente ON Servicio.id_Cliente = Cliente.id_Cliente"

        cursor.execute(sql)
        servicios = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convierte el resultado de la consulta en una lista de diccionarios
        columnas = ['id_Servicio', 'fecha_recogida', 'cantidad', 'tipo_servicio', 'tipo_prenda', 'nombre_cliente', 'apellido_cliente']
        servicios_list = [dict(zip(columnas, servicio)) for servicio in servicios]

        return servicios_list

    # Retorna una lista vacía si hay algún problema con la conexión a la base de datos
    return []

