from DB.conexion import obtener_conexion



async def insertar_usuario(telefono):
    try:
        #conexion a la base de datos
        conexion =  obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql
        sql = f"INSERT INTO usuario (telefono) VALUES ({telefono});"
        
        # Ejecutamos la query
        await cursor.execute(sql)

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

async def insertar_ingreso(telefono,monto_ingreso):
    try:
        #conexion a la base de datos
        conexion = obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql para buscar el id del usuario mediante su telefono
        sql = f"SELECT id FROM usuario WHERE telefono = CAST({telefono} AS CHARACTER VARYING)"
        
        # ejecutamos la query y la guardamos en una variable
        await cursor.execute(sql)

        id_usuario= cursor.fetchone()[0] # cursor.fetchone me devuelve una tupla, tomo el elemento con [0]
        
        
        # crear sentencia sql para agregar el ingreso

        sql = f"INSERT INTO ingreso (id_usuario,monto_ingreso,fecha) VALUES ({id_usuario},{monto_ingreso},CURRENT_TIMESTAMP) "


        # Ejecutamos la query
        await cursor.execute(sql)
        

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

async def insertar_gasto(telefono,monto_gasto):
    try:
        #conexion a la base de datos
        conexion = obtener_conexion()
        
        #utlizar cursor
        cursor = conexion.cursor()
        
        # crear sentencia sql para buscar el id del usuario mediante su telefono
        sql = f"SELECT id FROM usuario WHERE telefono = CAST({telefono} AS CHARACTER VARYING)"
        
        # ejecutamos la query y la guardamos en una variable
        await cursor.execute(sql)

        id_usuario=cursor.fetchone()[0] # cursor.fetchone me devuelve una tupla, tomo el elemento con [0]
        
        
        # crear sentencia sql para agregar el ingreso

        sql = f"INSERT INTO gasto (id_usuario,monto_gasto,fecha) VALUES ({id_usuario},{monto_gasto},CURRENT_TIMESTAMP) "


        # Ejecutamos la query
        await cursor.execute(sql)
        

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
        await cursor.execute(sql)

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
        await cursor.execute(sql)
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
        await cursor.execute(sql)
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
        await cursor.execute(sql)
        registro = cursor.fetchall()
        conexion.commit
        cursor.close()
        conexion.close()
        return registro
    
    except Exception as e:
        print ("Error: "+ str(e)) 

"""if __name__== "__main__":
    #insertar_usuario("+111222333")

    id = buscar_id_por_telefono("542604331853")
    ingresos = seleccionar_ingresos_porID(id)
    data = ""
    for item in ingresos:
        fecha = str(item[3])
        monto = str(item[2])
        #print(fecha[:10]," - $",str(item[2]))
        data = data + f"{fecha[:10]} - ${monto}\n"
    print(data)"""