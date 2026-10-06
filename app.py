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

@app.route("/clientes")
def clientes():
    conn = get_db_connection()  # Abrimos la conexion, y guardamos en la variable "conn".
    clientes = conn.execute('select * from clientes').fetchall() # Usamos la conexion para consultar los datos.
    conn.close()    # Cerramos la conexion.
    return render_template('clientes.html', clientes= clientes) # Enviamos los datos a la vista.

@app.route("/vehiculos")
def vehiculos():
    conn = get_db_connection()
    vehiculos = conn.execute('select * from vehiculos').fetchall()
    conn.close()
    return render_template('vehiculos.html', vehiculos= vehiculos)

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




if __name__ == "__main__":
    app.run(debug=True)
