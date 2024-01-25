
import json
import sett
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
    headers = {
        "Authorization": "Bearer " + whatsapp_token,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            print(headers)
            print("se envia", data)

            async with session.post(whatsapp_url,headers = headers, data = data) as response:
                if response.status == 200:
                    print("Status:", response.status)
                else:
                    contenido_error = await response.text()
                    print(f"Error en enviar mensaje: {response.status}, Contenido{contenido_error}")

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
        options = ["registrar ingreso","registrar gasto","más opciones"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        
      
        list.append(replyButtonData)
   
   
    elif "ingreso_registrado" in text:
        body = "Ingreso registrado exitosamente, ¿quieres realizar otra accion?"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","más opciones"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed2", messageId)
        list.append(replyButtonData)  


    elif "gasto_registrado" in text:
        body = "Gasto registrado exitosamente, ¿quieres realizar otra accion?"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","más opciones"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)  


    elif text == "resultado neto":
        resultado_neto = await cont.resultado_neto(number)
        #data = text_Message(number, resultado_neto)
        # list.append(data)

        body = f"{resultado_neto}"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","más opciones"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4", messageId)
        list.append(replyButtonData)


    elif text == "mostrar ingresos":
        ingresos = await cont.pedir_ingresos(number)
        #data = text_Message(number,ingresos)
            
        body = f"{ingresos}"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","más opciones"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed5", messageId)
        list.append(replyButtonData)   


    elif text == "mostrar gastos":
        gastos = await cont.pedir_gastos(number)
        body = f"{gastos}"
        footer = "WALLET"
        options = ["registrar ingreso","registrar gasto","más opciones"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed6", messageId)
        list.append(replyButtonData)

    elif text == "más opciones":
        
        body = "Aquí hay mas opciones:"
        footer = "WALLET"
        options = ["resultado neto","mostrar ingresos","mostrar gastos"]

        replyButtonData = buttonReply_Message(number,options,body,footer,"sed7",messageId)
        list.append(replyButtonData)
    
    elif  text=="registrar ingreso":
        data = text_Message(number, "Digite el monto:")
        sett.esperando_monto = True
        sett.ingreso = True
        sett.gasto = False
        list.append(data)
    


    elif text=="registrar gasto":
        data = text_Message(number, "Digite el monto:")
        sett.esperando_monto = True
        sett.gasto = True
        sett.ingreso = False
        list.append(data)
        
    elif  text=="agregar_nota":
        data = text_Message(number, "Agregue una nota:")
        sett.esperando_nota = True
        list.append(data)
    else : 
        body = "Lo siento, no entendi lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?"
        footer = "WALLET"
        options = ["resultado neto","mostrar ingresos","mostrar gastos"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed7", messageId)
        list.append(replyButtonData)

    
    for item in list:
        await enviar_Mensaje_whatsapp(item)