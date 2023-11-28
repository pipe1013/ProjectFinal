# index.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import Blueprint, render_template
from db import connect_to_db
import mysql.connector


cliente_routes = Blueprint('cliente', __name__)

# Añadir esta importación al principio del archivo
from datetime import datetime

# Modificar la función cliente en cliente.py
@cliente_routes.route('/cliente')
def cliente():
    user_data = session.get('user_data', None)

    if user_data and session['user_role'] == 'cliente':
        # Obtener pedidos del cliente desde la base de datos
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()

            # Consulta para obtener los pedidos del cliente
            sql_pedidos = """
                SELECT s.id_Servicio, s.fecha_recogida, s.cantidad, ts.nombre as tipo_servicio, tp.nombre as tipo_prenda
                FROM Servicio s
                JOIN Tipo_de_Servicio ts ON s.id_TipoServicio = ts.id_TipoServicio
                JOIN Tipo_de_Prenda tp ON s.id_Prenda = tp.id_Prenda
                WHERE s.id_Cliente = %s
            """
            cursor.execute(sql_pedidos, (user_data['id_Cliente'],))
            pedidos = cursor.fetchall()

            cursor.close()
            conn.close()

            # Convertir la fecha de recogida a formato legible
            for i, pedido in enumerate(pedidos):
                pedidos[i] = (pedido[0], pedido[1].strftime('%Y-%m-%d'), pedido[2], pedido[3], pedido[4])

            return render_template('cliente.html', user_data=user_data, pedidos=pedidos)
    else:
        # Manejar el caso en el que el usuario no esté autenticado como cliente
        return redirect(url_for('login.login'))


@cliente_routes.route('/ver_perfil', methods=['GET'])
def ver_perfil():
    user_data = session.get('user_data', None)

    if user_data and session['user_role'] == 'cliente':
        return render_template('ver_perfil.html', user_data=user_data)
    else:
        # Manejar el caso en el que el usuario no esté autenticado como cliente
        return redirect(url_for('login.login'))

@cliente_routes.route('/editar_perfil', methods=['POST'])
def editar_perfil():
    user_id = session['user_data']['id_Cliente']
    new_nombre = request.form['nombre']
    new_apellido = request.form['apellido']
    new_telefono = request.form['telefono']
    new_direccion = request.form['direccion']

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Actualizar los datos del cliente en la base de datos
        sql_update = "UPDATE Cliente SET nombre = %s, apellido = %s, telefono = %s, direccion = %s WHERE id_Cliente = %s"
        cursor.execute(sql_update, (new_nombre, new_apellido, new_telefono, new_direccion, user_id))
        conn.commit()

        cursor.close()
        conn.close()

        # Actualizar los datos en la sesión
        session['user_data']['nombre'] = new_nombre
        session['user_data']['apellido'] = new_apellido
        session['user_data']['telefono'] = new_telefono
        session['user_data']['direccion'] = new_direccion

    # Redirigir a la página de ver_perfil
    return redirect(url_for('cliente.ver_perfil'))


@cliente_routes.route('/agendar_pedido', methods=['GET', 'POST'])
def agendar_pedido():
    if request.method == 'POST':
        # Lógica para procesar el formulario
        fecha_recogida = request.form['fecha_recogida']
        cantidad = request.form['cantidad']
        tipo_servicio = request.form['tipo_servicio']
        tipo_prenda = request.form['tipo_prenda']

        # Lógica para insertar el servicio en la base de datos
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()

            # Insertar el servicio en la base de datos
            sql_insert = "INSERT INTO Servicio (fecha_recogida, cantidad, id_TipoServicio, id_Prenda, id_Cliente) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, (fecha_recogida, cantidad, tipo_servicio, tipo_prenda, session['user_data']['id_Cliente']))
            conn.commit()

            cursor.close()
            conn.close()

            # Redirigir a la página de ver_perfil después de agendar el servicio
            return redirect(url_for('cliente.ver_perfil'))

    # Lógica para obtener opciones de tipo de servicio y tipo de prenda desde la base de datos
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Obtener opciones de tipo de servicio desde la base de datos
        sql_tipo_servicio = "SELECT id_TipoServicio, nombre FROM Tipo_de_Servicio"
        cursor.execute(sql_tipo_servicio)
        tipo_servicio_options = cursor.fetchall()

        # Obtener opciones de tipo de prenda desde la base de datos
        sql_tipo_prenda = "SELECT id_Prenda, nombre FROM Tipo_de_Prenda"
        cursor.execute(sql_tipo_prenda)
        tipo_prenda_options = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('agendar_pedido.html', tipo_servicio_options=tipo_servicio_options, tipo_prenda_options=tipo_prenda_options)

    # Lógica para listar clientes u otras operaciones GET
    return render_template('agendar_pedido.html')
