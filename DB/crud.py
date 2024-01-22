import asyncio
from DB.conexion import obtener_conexion

#from conexion import obtener_conexion

async def insertar_usuario(telefono):
    try:
        #conexion a la base de datos
        conexion =  obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql
        sql = f"INSERT INTO usuario (telefono) VALUES ({telefono});"
        
        # Ejecutamos la query
        cursor.execute(sql)

        # guardamos registros
        conexion.commit()

        # registros insertados
        registros = cursor.rowcount

        print(f"registros insertados: {registros}")

        #cerrar conexiones
        cursor.close()
        conexion.close()
    except Exception as e:
        print(e)

async def insertar_ingreso(telefono,monto_ingreso,nota):
    try:
        #conexion a la base de datos
        conexion = obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql para buscar el id del usuario mediante su telefono
        sql = f"SELECT id FROM usuario WHERE telefono = CAST({telefono} AS CHARACTER VARYING)"
        
        # ejecutamos la query y la guardamos en una variable
        cursor.execute(sql)

        id_usuario= cursor.fetchone()[0] # cursor.fetchone me devuelve una tupla, tomo el elemento con [0]
        
        
        # crear sentencia sql para agregar el ingreso y agregar nota

        str_nota = str(nota)
        sql = f"INSERT INTO ingreso (id_usuario,monto_ingreso,fecha,nota) VALUES ({id_usuario},{monto_ingreso},CURRENT_TIMESTAMP,'{str_nota}')"


        # Ejecutamos la query
        cursor.execute(sql)
        

        # guardamos registros
        conexion.commit()

        # registros insertados
        registros = cursor.rowcount

        print(f"registros insertados: {registros}")

        #cerrar conexiones
        cursor.close()
        conexion.close()
    except Exception as e:
        print(e)

async def insertar_gasto(telefono,monto_gasto,nota):
    try:
        #conexion a la base de datos
        conexion = obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql para buscar el id del usuario mediante su telefono
        sql = f"SELECT id FROM usuario WHERE telefono = CAST({telefono} AS CHARACTER VARYING)"
        
        # ejecutamos la query y la guardamos en una variable
        cursor.execute(sql)

        id_usuario=cursor.fetchone()[0] # cursor.fetchone me devuelve una tupla, tomo el elemento con [0]
        
        
        # crear sentencia sql para agregar el ingreso

        str_nota = str(nota)
        sql = f"INSERT INTO gasto (id_usuario,monto_gasto,fecha,nota) VALUES ({id_usuario},{monto_gasto},CURRENT_TIMESTAMP,'{str_nota}')"


        # Ejecutamos la query
        cursor.execute(sql)
        

        # guardamos registros
        conexion.commit()

        # registros insertados
        registros = cursor.rowcount

        print(f"registros insertados: {registros}")

        #cerrar conexiones
        cursor.close()
        conexion.close()
    except Exception as e:
        print(e)

async def verificar_existencia(telefono):
    try:
        #conexion a la base de datos
        conexion =  obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql
        sql = f"SELECT * FROM usuario WHERE telefono = CAST({telefono} AS CHARACTER VARYING)"

        # Ejecutamos la query
        cursor.execute(sql)

        # guardamos registros
        conexion.commit()

        # registros insertados
        registros = cursor.fetchone()

        #cerrar conexiones
        cursor.close()
        conexion.close()

        if registros is not None:
            print("Usuario encontrado")
            return True
        else:
            print("Usuario no encontrado")
            return False
    except Exception as e:
        print(e)

async def buscar_id_por_telefono(telefono):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql=f"SELECT id FROM usuario WHERE telefono = CAST({telefono} AS CHARACTER VARYING)"
        cursor.execute(sql)
        registro = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        if registro is not None:
            print("Usuario encontrado")
            return registro
        else:
            print("Usuario no encontrado")

    except Exception as e:
        print ("Error: "+ str(e))

async def seleccionar_ingresos_porID(id):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql=f"SELECT * FROM ingreso WHERE id_usuario = CAST({id} AS INTEGER)"
        
        cursor.execute(sql)
        registro = cursor.fetchall()
        conexion.commit
        cursor.close()
        conexion.close()
        return registro

       
    except Exception as e:
        print ("Error: "+ str(e)) 

async def seleccionar_gastos_porID(id):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql=f"SELECT * FROM gasto WHERE id_usuario = CAST({id} AS INTEGER)"
        cursor.execute(sql)
        registro = cursor.fetchall()
        conexion.commit
        cursor.close()
        conexion.close()
        return registro
    
    except Exception as e:
        print ("Error: "+ str(e)) 

if __name__== "__main__":
    #insertar_usuario("+111222333")
    async def __main__():
        await ej()
    async def ej():

        id = await buscar_id_por_telefono("542604331853")
        ingresos = await asyncio.gather(seleccionar_ingresos_porID(id))
        
        data = f""
        for lista in ingresos:
            for tupla in lista:
                fecha = str(tupla[2])
                monto = str(tupla[1])
                nota = str(tupla[3])
                #print(fecha[:10]," - $",str(item[2]))
                data = data + f"{fecha[:10]} - ${monto} - {nota}\n"
        print(ingresos)
        print("")            
        print(data)
   
    asyncio.run(__main__())