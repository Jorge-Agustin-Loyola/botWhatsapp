import asyncio
import DB.crud as crud
import json

async def pedir_ingresos(telefono):
    id = await crud.buscar_id_por_telefono(telefono)
    ingresos = await crud.seleccionar_ingresos_porID(id)
    data = ""
    for item in ingresos:
        fecha = str(item[3])
        monto = str(item[2])
        #print(fecha[:10]," - $",str(item[2]))
        data = data + f"{fecha[:10]} - ${monto}\n"
    return data

async def pedir_gastos(telefono):
    id = await crud.buscar_id_por_telefono(telefono)
    gastos = await crud.seleccionar_gastos_porID(id)
    data = ""
    for item in gastos:
        fecha = str(item[3])
        monto = str(item[2])
        #print(fecha[:10]," - $",str(item[2]))
        data = data + f"{fecha[:10]} - ${monto}\n"
    return data

async def resultado_neto(telefono):
    id = await crud.buscar_id_por_telefono(telefono)
    ingresos = await asyncio.gather(crud.seleccionar_ingresos_porID(id))
    gastos = await asyncio.gather(crud.seleccionar_gastos_porID(id))
    total_gasto = 0
    total_ingreso = 0
    #suma los ingresos del usuario
    for lista in ingresos:
        for tupla in lista:
            total_ingreso = total_ingreso + int(tupla[1])  # item[2] devuelve el monto del registro de ingresos 
    #suma los gastos del usuario
    for lista in gastos:
        for tupla in lista:
            total_gasto = total_gasto + int(tupla[1]) 
    
    # suma de ganacias y gastos
    resultado_neto = total_ingreso - total_gasto 

    if resultado_neto>0:
        signo= "+"
    elif resultado_neto == 0:
        signo = ""
    else:
        signo= "-"
    
    data = f"Ingresos: ${total_ingreso}\nGastos: ${total_gasto}\nResultado_neto: {signo}${resultado_neto}"

    return data

