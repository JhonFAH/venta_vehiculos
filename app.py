import sqlite3  #Importamos la libreria

#creamos la BDD venta_vehiculos.
conn = sqlite3.connect('venta_vehiculos.db')
# =====================================
# CREACION DE TABLAS
# ====================================
# TABLA VEHICULOS.
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS vehiculos(
        vehiculo_id INTEGER PRIMARY KEY,
        modelo TEXT NOT NULL,
        placa TEXT NOT NULL,
        color TEXT NOT NULL
    )
    """
)
# TABLA CLIENTES.
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS clientes(
        cliente_id INTEGER PRIMARY KEY,
        nombres TEXT NOT NULL,
        apellidos TEX NOT NULL,
        ci TEXT NOT NULL
        
    )
    """
)
# TABLA VENTAS.
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS ventas(
        venta_id INTEGER PRIMARY KEY,
        fecha_venta DATE NOT NULL,
        vehiculo_id INTEGER NOT NULL,
        cliente_id INTEGER NOT NULL,
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    )
    """
)


# ========================================
# INSERTAR DATOS EN TABLAS
# ========================================


# # insertamos a VEHICULOS.
# conn.execute(
#     """
#         INSERT INTO vehiculos(modelo,placa,color)
#         VALUES ('Toyota Corolla', '1234ABC', 'Blanco'),
#                 ('Nissan Sentra', '5678DEF', 'Negro'),
#                 ('Honda Civic', '9012GHI', 'Gris'),
#                 ('Hyundai Tucson', '3456JKL', 'Rojo'),
#                 ('Kia Sportage', '7890MNO', 'Azul'),
#                 ('Suzuki Suzuki', '2345PQR', 'Plata'),
#                 ('Chevrolet Spark', '6789STU', 'Verde'),
#                 ('Volkswagen Gol', '0123VWX', 'Blanco'),
#                 ('Ford Ranger', '4567YZA', 'Negro'),
#                 ('Mazda CX-5', '8901BCD', 'Granate')
#     """
# )
# conn.commit()   # Confirmamos las transacciones.


# # Insertamos a CLIENTES.
# conn.execute(
#     """
#         INSERT INTO clientes(nombres,apellidos,ci)
#         VALUES('Bruno','Diaz','12345678LP'),
#             ('Juan','Pinto','22222222OR'),
#             ('Maria','Fernandez','33333333LP'),
#             ('Julia','Ramirez','44444444LP'),
#             ('Geraldine','Rios','55555555LP'),
#             ('Reynaldo','Mamani','77777777LP'),
#             ('Efrain','Sanchez','88888888LP'),
#             ('Angel','Apaza','99999999LP'),
#             ('Eugenia','Condori','12344444TJ'),
#             ('Eliana','Mamani','55443322LP')
#     """
# )
# conn.commit()   # Confirmamos las transacciones.

# # Insertamos a VENTAS.
# conn.execute(
#     """
#         INSERT INTO ventas(fecha_venta, vehiculo_id, cliente_id)
#         VALUES('01-01-2026',1,1),
#             ('04-01-2026',2,2),
#             ('14-01-2026',3,3),
#             ('24-02-2026',4,4),
#             ('28-03-2026',5,5),
#             ('22-04-2026',6,6),
#             ('03-05-2026',7,7)
#     """
# )
# conn.commit()   # Confirmamos las transacciones.


# ======================================
# CURSORES, para ver los datos.
# ======================================

#Creamos un curso, para mostrar VEHICULOS.
print("\n VEHICULOS")
cursor = conn.execute("SELECT * FROM vehiculos")
for row in cursor:
    print (row)
    

# Creamos un curso, para mostrar CLIENTES.
print("\n CLIENTES")
cursor = conn.execute("SELECT * FROM clientes")
for row in cursor:
    print (row)

# Creamos un curso, para mostrar VENTAS.
print("\n VENTAS")
cursor = conn.execute("SELECT * FROM ventas")
for row in cursor:
    print (row)




