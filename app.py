from flask import Flask, request, redirect, render_template,url_for,flash

import sqlite3  #Importamos la libreria

app = Flask(__name__)
app.secret_key = 'unaClaveSecreta'

# FUncion para conectar a la base de datos.
def get_db_connection():
    conn = sqlite3.connect("venta_vehiculos.db")    # Transformamos los datos a diccionarios.
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return redirect(url_for('clientes'))

# =================================================
#  funcion INDEX, mostramos la lista completa de registros.
# ==================================================

# Cliente
@app.route("/clientes")
def clientes():
    conn = get_db_connection()  # Abrimos la conexion, y guardamos en la variable "conn".
    clientes = conn.execute('select * from clientes').fetchall() # Usamos la conexion para consultar los datos.
    conn.close()    # Cerramos la conexion.
    return render_template('clientes.html', clientes= clientes) # Enviamos los datos a la vista.

# Vehiculo
@app.route("/vehiculos")
def vehiculos():
    conn = get_db_connection()
    vehiculos = conn.execute('select * from vehiculos').fetchall()
    conn.close()
    return render_template('vehiculos.html', vehiculos= vehiculos)

# Vnta
@app.route("/ventas")
def ventas():
    conn = get_db_connection() # Abrimos la conexion.
    ventas = conn.execute(
        """
            select v.venta_id,
                v.fecha_venta,
                c.nombres ||' '|| c.apellidos as cliente,
                vh.modelo ||' '|| vh.placa as vehiculo
            from ventas v
            join clientes c ON v.cliente_id = c.cliente_id
            join vehiculos vh ON v.vehiculo_id = vh.vehiculo_id
        """
    ).fetchall() # Usamos la conexion.
    conn.close()    # Cerramos la conexion.
    return render_template('ventas.html', ventas=ventas ) # Enviamos datos a la vista.

# =====================================
# funciones CREATE y STORE, añadir nuevos registros
# ====================================

# Nuevo vehiculo
@app.route("/vehiculo/nuevo",methods=['GET','POST'])
def nuevo_vehiculo():
    if request.method == 'POST':
        # Leer contenido del formulario
        modelo = request.form['modelo']
        placa = request.form['placa']
        color = request.form['color']
    
        conn = get_db_connection()
        
        # Verificar si la placa ya existe registrada
        existe_placa = conn.execute(
            "SELECT 1 FROM vehiculos WHERE placa = ? LIMIT 1", (placa,)
        ).fetchone()
        
        if existe_placa:
            conn.close()
            flash('Error: Ya existe un vehículo registrado con esa placa.', 'danger')
            return render_template('form_vehiculos.html')
        
        conn.execute("insert into vehiculos(modelo,placa,color) values (?,?,?)",(modelo,placa,color))
        conn.commit()
        conn.close()
        flash('Vehiculo agregado correctamente','success')
        
        return redirect(url_for('vehiculos'))
        
    return render_template('form_vehiculos.html')

# Nueva Venta
@app.route("/venta/nuevo",methods=['GET','POST'])
def nueva_venta():
    conn = get_db_connection()
    # En caso que sea POST, consolidar la venta.
    if request.method == 'POST':
            # Leer contenido del formulario
            fecha_venta = request.form['fecha_venta']
            vehiculo_id = request.form['vehiculo_id']
            cliente_id = request.form['cliente_id']
            
            conn.execute(
                """
                insert into ventas
                (fecha_venta,vehiculo_id,cliente_id)
                values (?,?,?)
                
                """,(fecha_venta,vehiculo_id,cliente_id)
                
            )
            conn.commit()
            conn.close()
            flash('Venta agregada correctamente','success')
            return redirect(url_for('ventas'))
    
    
    # En caso de GET enviar datos para mostrar el formulario de venta.
    clientes = conn.execute(
        """
        select cliente_id,( nombres||' '|| apellidos) as nombre
        from clientes
        """        
    ).fetchall()
    
    # Filtramos los vehículos que NO estén en la tabla de ventas
    vehiculos = conn.execute(
        """
        SELECT vehiculo_id, (modelo || ' ' || placa || ' ' || color) AS descripcion
        FROM vehiculos
        WHERE vehiculo_id NOT IN (SELECT vehiculo_id FROM ventas)
        """
    ).fetchall()
    conn.close()
    
    return render_template('form_ventas.html',clientes=clientes, vehiculos=vehiculos)
    
# Nuevo Cliente
@app.route("/cliente/nuevo", methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        ci = request.form['ci']
    
        conn = get_db_connection()
        
        # Verificar si el CI ya existe
        existe_ci = conn.execute(
            "SELECT 1 FROM clientes WHERE ci = ? LIMIT 1", (ci,)
        ).fetchone()
        
        if existe_ci:
            conn.close()
            flash('Error: Ya existe un cliente registrado con ese número de C.I.', 'danger')
            return render_template('form_clientes.html')

        conn.execute("INSERT INTO clientes (nombres, apellidos, ci) VALUES (?, ?, ?)", (nombres, apellidos, ci))
        conn.commit()
        conn.close()
        flash('Cliente agregado correctamente', 'success')
        return redirect(url_for('clientes'))
        
    return render_template('form_clientes.html')
    
        
    



# =====================================
# funcion EDIT y UPDATE, editar y actualizamos registros.
# ====================================

# Editar Vehículo
@app.route('/vehiculo/editar/<int:id>', methods=['GET', 'POST'])
def editar_vehiculo(id):
    conn = get_db_connection()
    vehiculo = conn.execute("SELECT * FROM vehiculos WHERE vehiculo_id = ?", (id,)).fetchone()
    
    if request.method == 'POST':
        modelo = request.form['modelo']
        placa = request.form['placa']
        color = request.form['color']
    
        # Verificar si la placa ya la tiene OTRO vehículo diferente
        existe_placa = conn.execute(
            "SELECT 1 FROM vehiculos WHERE placa = ? AND vehiculo_id != ? LIMIT 1",
            (placa, id)
        ).fetchone()
        
        if existe_placa:
            conn.close()
            flash('Error: La placa ingresada ya pertenece a otro vehículo.', 'danger')
            # Mantenemos los datos ingresados
            return render_template('form_vehiculos.html', vehiculo={'vehiculo_id': id, 'modelo': modelo, 'placa': placa, 'color': color})
        
        # Si la placa está disponible, actualizamos
        conn.execute(
            "UPDATE vehiculos SET modelo = ?, placa = ?, color = ? WHERE vehiculo_id = ?",
            (modelo, placa, color, id)
        )
        conn.commit()
        conn.close()
        flash('Vehículo actualizado correctamente', 'success')
        return redirect(url_for('vehiculos'))
    
    conn.close()
    return render_template('form_vehiculos.html', vehiculo=vehiculo)


# Editar Cliente
@app.route('/cliente/editar/<int:id>',methods=['GET','POST'])
def editar_cliente(id):
    conn = get_db_connection()
    cliente = conn.execute("select * from clientes where cliente_id =?",(id,)).fetchone()
    
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        ci = request.form['ci']
    
        conn.execute("update clientes set nombres =?, apellidos=? , ci =? where cliente_id =?",(nombres,apellidos,ci,id))
    
        conn.commit()
        conn.close()
        flash('Datos del Cliente actualizado','success')
        return redirect(url_for('clientes'))
    
    conn.close()
    return render_template('form_clientes.html', cliente=cliente)

# Editar Venta
@app.route('/venta/editar/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        fecha_venta = request.form['fecha_venta']
        vehiculo_id = request.form['vehiculo_id']
        cliente_id = request.form['cliente_id']
        
        conn.execute(
            """
            UPDATE ventas 
            SET fecha_venta = ?, vehiculo_id = ?, cliente_id = ?
            WHERE venta_id = ?
            """, (fecha_venta, vehiculo_id, cliente_id, id)
        )
        conn.commit()
        conn.close()
        flash('Venta actualizada correctamente', 'success')
        return redirect(url_for('ventas'))
    
    
    venta = conn.execute(
        """
        SELECT venta_id, fecha_venta, cliente_id, vehiculo_id 
        FROM ventas 
        WHERE venta_id = ?
        """, (id,)
    ).fetchone()
    print("FECHA:", venta['fecha_venta'])
    clientes = conn.execute("SELECT cliente_id, (nombres || ' ' || apellidos) AS nombre FROM clientes").fetchall()
    
    # Incluye los vehículos disponibles Y el vehículo asignado a esta venta actual
    vehiculos = conn.execute(
        """
        SELECT vehiculo_id, ('PLACA: ' || placa || ' - ' || modelo || ' (' || color || ')') AS descripcion
        FROM vehiculos
        WHERE vehiculo_id NOT IN (SELECT vehiculo_id FROM ventas WHERE venta_id != ?)
        """, (id,)
    ).fetchall()
    
    conn.close()
    return render_template('form_ventas.html', venta=venta, clientes=clientes, vehiculos=vehiculos)


# =====================================
# funcion DELETE, eliminamos registros.
# ====================================

# Eliminar Vehículo
@app.route('/vehiculo/eliminar/<int:id>')
def eliminar_vehiculo(id):
    conn = get_db_connection()  # Abrimos la conexión a la BDD
    
    # Verificamos si el vehículo ya está registrado en alguna venta
    vehiculo_vendido = conn.execute(
        "SELECT 1 FROM ventas WHERE vehiculo_id = ? LIMIT 1", (id,)
    ).fetchone()
    
    # Si ya fue vendido, bloqueamos la eliminación y mostramos el mensaje de advertencia
    if vehiculo_vendido:
        conn.close()
        flash('No se puede eliminar el vehículo porque ya está registrado en una venta.', 'danger')
        return redirect(url_for('vehiculos'))
    
    # Si no ha sido vendido, lo eliminamos normalmente
    conn.execute("DELETE FROM vehiculos WHERE vehiculo_id = ?", (id,))
    
    conn.commit()
    conn.close()
    
    flash('Vehículo eliminado correctamente.', 'success')
    return redirect(url_for('vehiculos'))

# Eliminar venta
@app.route('/venta/eliminar/<int:id>')
def eliminar_venta(id):
    conn = get_db_connection()  # abrimos la conexion a la BDD
    conn.execute("delete from ventas where venta_id=?",(id,))
    
    conn.commit()
    conn.close()
    flash('Venta eliminada', 'success')

    return redirect(url_for('ventas'))

# Eliminar Cliente
@app.route('/cliente/eliminar/<int:id>')
def eliminar_cliente(id):
    conn = get_db_connection()  # Abrimos la conexión a la BDD
    
    #  Verificamos si existen ventas asociadas a este cliente
    venta_existente = conn.execute(
        "SELECT 1 FROM ventas WHERE cliente_id = ? LIMIT 1", (id,)
    ).fetchone()
    
    #  Si la consulta devuelve algo, el cliente tiene ventas y detengamos el borrado
    if venta_existente:
        conn.close()
        flash('No se puede eliminar el cliente porque tiene ventas asociadas.', 'danger')
        return redirect(url_for('clientes'))
    
    # Si no tiene ventas, procedemos con el borrado
    conn.execute("DELETE FROM clientes WHERE cliente_id = ?", (id,))
    
    conn.commit()
    conn.close()
    
    flash('Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes'))



if __name__ == "__main__":
    app.run(debug=True)
