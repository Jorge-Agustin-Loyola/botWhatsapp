from decouple import config
import psycopg2

#conexon a base de datos
def obtener_conexion():

    conexion =  psycopg2.connect(
        user= config('USER'),
        password = config('PASSWORD'),
        host = config('HOST'),
        port = config('PORT'),
        database= config('DATABASE')
    )
    return conexion