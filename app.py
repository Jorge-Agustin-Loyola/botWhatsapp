from flask import Flask, request
import sett
import services
import DB.crud as crud


from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
#########migraciones############################################
app.config['SQLALCHEMY_DATABASE_URI'] = config('FULL_URL_DB')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
################################################################


@app.route('/bienvenido', methods = ['GET'])
def bienvenido():
    return 'Hola desde flask'
            
@app.route('/webhook', methods = ['GET'])    
def verificar_token():
    if request.method == 'GET':

        try:
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            if token == sett.token:
             return challenge
            else:
             return 'token incorrectooo', 403
        except Exception as e:
            return e, 403

@app.route('/webhook', methods = ['POST']) 
async def recibir_mensaje():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        messages = value['messages'][0]
        number = messages['from']
        # corrijo el número
        number = number.replace("549","54")
        messageId = messages['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(messages)

        

        # si el usuario no existe se guarda en la base de datos
        if await crud.verificar_existencia(number):
            if sett.esperando_monto and sett.ingreso:
                if sett.esperando_nota == False:
                    sett.monto = text
                    await services.administrar_chatbot("agregar_nota",number,messageId,name)
                    return 'monto digitado - esperando nota'
                else:
                    sett.nota = text
                
                    await crud.insertar_ingreso(number,sett.monto,sett.nota)
                    sett.esperando_monto = False
                    sett.esperando_nota = False
                    await services.administrar_chatbot("ingreso_registrado",number,messageId,name)
                    return 'ingreso registrado'
            elif sett.esperando_monto and sett.gasto:
                if sett.esperando_nota == False:
                    sett.monto = text
                    await services.administrar_chatbot("agregar_nota",number,messageId,name)
                    return 'monto digitado - esperando nota'
                else:
                    sett.nota = text

                    await crud.insertar_gasto(number,sett.monto,sett.nota)
                    sett.esperando_monto = False
                    sett.esperando_nota = False
                    await services.administrar_chatbot("gasto_registrado",number,messageId,name)
                    return 'gasto registrado'
            else:
                await services.administrar_chatbot(text,number,messageId,name)
                return 'enviado'
        else:
            await crud.insertar_usuario(number)
            if await crud.verificar_existencia(number):
                await services.administrar_chatbot(text,number,messageId,name)

            return 'Se agrego un contacto'

    except Exception as e:
        return 'no enviado ' + str(e)

