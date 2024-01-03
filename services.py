import time
import json
import  sett
import aiohttp
import contador as cont


def obtener_Mensaje_whatsapp(messages):
    if 'type' not in messages: 
        text = 'mensaje no reconocido'
    
    typeMessage = messages['type']
    if typeMessage == 'text':
        text = messages['text']['body']
    elif typeMessage == "button":
        text = messages["button"]["text"]
    elif typeMessage == "interactive" and messages["interactive"]["type"] == "list_reply":
        text = messages["interactive"]["list_reply"]["title"]
    elif typeMessage == "interactive" and messages["interactive"]["type"] == "button_reply":
        text = messages["interactive"]["button_reply"]["title"]
    else:
        text = "mensaje no reconocido"

    
    return text

async def enviar_Mensaje_whatsapp(data):

    whatsapp_token = sett.whatsapp_token
    whatsapp_url = sett.whatsapp_url
    headers = {'Content-Type': 'application/json',
                'Authorization':'Bearer ' + whatsapp_token}

    async with aiohttp.ClientSession() as session:
        try:
            print("se envia", data)
            async with session.post(whatsapp_url, data = data, headers = headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                else:
                    print(response.status)

        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))

def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
        )
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []

    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data =  {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                 "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }   

    data = json.dumps(data)
    
    return data
   
def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )
    
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    data = json.dumps(data)
    return data

def document_Messages(number, url, caption, filname):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filname": filname
            }
        }
    data = json.dumps(data)
    return data

def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "image":
        media_id = sett.image.get[media_name, None]
    elif media_type == "video":
        media_id = sett.video.get[media_name, None]
    elif media_type == "audio":
        media_id = sett.audio.get[media_name, None]
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    data = json.dumps(data)
    return data

def replyText_Message(number, messageId, text):
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            "type": "text",
            "text": {
                "body": text
            }
        }
    data = json.dumps(data)
    return data

def markRead_Message(messageId):
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": messageId
      }
    data = json.dumps(data)
    return data

async def administrar_chatbot(text, number, messageId,name):

    
    list = []

    if "hola" in text:
        body = "¡Hola 👋 Bienvendo, ¿Como podemos ayudarte hoy?"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","ver resultado_neto"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",
        messageId)
        
      
        list.append(replyButtonData)
        
    elif  text=="registrar ingreso":
        data = text_Message(number, "Digite el monto:")
        sett.esperando_monto = True
        sett.ingreso = True
        sett.gasto = False
        list.append(data)

    elif "ingreso_registrado" in text:
        body = "Ingreso registrado exitosamente, ¿quieres realizar otra accion?"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","ver resultado_neto"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2",
        messageId)
        list.append(replyButtonData)
    
    elif text == "mostrar ingresos":
        ingresos = cont.pedir_ingresos(number)
        data = text_Message(number,ingresos)
        list.append(data)
    elif text == "mostrar gastos":
        gastos = cont.pedir_gastos(number)
        data = text_Message(number,gastos)
        list.append(data)
        
    
    elif text=="registrar gasto":
        data = text_Message(number, "Digite el monto:")
        sett.esperando_monto = True
        sett.gasto = True
        sett.ingreso = False
        list.append(data)
        
    elif "gasto_registrado" in text:
        body = "Gasto registrado exitosamente, ¿quieres realizar otra accion?"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","ver resultado neto"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",
        messageId)
        list.append(replyButtonData)

    
    elif text == "ver resultado neto":
        resultado_neto = cont.resultado_neto(number)
        data = text_Message(number,resultado_neto)
        list.append(data)

        
    else : 
        data = text_Message(number, "Lo siento, no entendi lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)
    
    for item in list:
        await enviar_Mensaje_whatsapp(item)