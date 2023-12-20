import psycopg2

#conexon a base de datos
def obtener_conexion():

    conexion = psycopg2.connect(
        user='postgres',
        password = 'agus462895',
        host = 'localhost',
        port = '5432',
        database= 'wallet'
    )
    return conexion