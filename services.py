import requests
import sett
import documents
import json
import time

# Para argentina al recibir el numero llega '549..' pero para enviar se encesita '54..'   
def replace_start(s):
    if s.startswith("549"):
        return "54" + s[3:]
    return s

def obtener_mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    return text

def enviar_mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_message(number,text):
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

def buttonReply_Message(number, options, body, footer, sedd,messageId):
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

    data = json.dumps(
        {
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
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
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
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = documents.stickers.get(media_name, None)
    elif media_type == "image":
        media_id = documents.images.get(media_name, None)
    elif media_type == "video":
        media_id = documents.videos.get(media_name, None)
    elif media_type == "audio":
        media_id = documents.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def send_location(number, latitude, longitude, location_name, adress):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": location_name,
                "address": adress
            }
        }
    )
    return data
  
    
def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)

        
    if "calendario academico" in text:
        print('calendario academico')
        body = "Aqui esta el PDF con el calendario academico 2023"
        footer = "@UTNRosario"

        document = document_Message(number, documents.calendario_academico_23, "Listo 👍🏻", "calendario_academico_2023.pdf")
        list.append(document)
        
    elif "plan de estudios" in text:
        body = "Seleccione la carrera."
        footer = "@UTNRosario"
        options = ["Ing. en Sist. de inf.", "Ing. Quimica", "Ing. Civil", "Ing. Electrica", "Ing. Mecanica"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)

        list.append(listReplyData)
        
    elif "sist. de inf." in text:
        print('pdf isi')

        document = document_Message(number, documents.plan_estudio_isi_08, "Plan de estudio 2008 Ingenieria en Sistemas de Informacion", "Plan_estudio_isi_08.pdf")
        list.append(document)
        document = document_Message(number, documents.plan_estudio_isi_23, "Plan de estudio 2023 Ingenieria en Sistemas de Informacion", "Plan_estudio_isi_23.pdf")
        list.append(document)
        
    elif "ing. quimica" in text:
        print('pdf iq')

        document = document_Message(number, documents.plan_estudio_iq_94, "Plan de estudio 1994 Ingenieria Quimica", "Plan_estudio_iq_94.pdf")
        list.append(document)
        document = document_Message(number, documents.plan_estudio_iq_23, "Plan de estudio 2023 Ingenieria Quimica", "Plan_estudio_iq_23.pdf")
        list.append(document)
        
    elif "ing. civil" in text:
        print('pdf ic')

        document = document_Message(number, documents.plan_estudio_ic_94, "Plan de estudio 1994 Ingenieria Civil", "Plan_estudio_ic_94.pdf")
        list.append(document)
        document = document_Message(number, documents.plan_estudio_iq_23, "Plan de estudio 2023 Ingenieria Civil", "Plan_estudio_ic_23.pdf")
        list.append(document)
        
    elif "ing. electrica" in text:
        print('pdf ie')

        document = document_Message(number, documents.plan_estudio_ie_94, "Plan de estudio 1994 Ingenieria Electrica", "Plan_estudio_ie_94.pdf")
        list.append(document)
        document = document_Message(number, documents.plan_estudio_ie_23, "Plan de estudio 2023 Ingenieria Electrica", "Plan_estudio_ie_23.pdf")
        list.append(document)
        
    elif "ing. mecanica" in text:
        print('pdf im')

        document = document_Message(number, documents.plan_estudio_im_23, "Plan de estudio 2023 Ingenieria Mecanica", "Plan_estudio_im_23.pdf")
        list.append(document)
        
    elif "horarios" in text:
        print('Horarios')
        body = "Seleccione el año de cursado."
        footer = "@UTNRosario"
        options = ["1.º año", "2.º año", "3.º año", "4.º año", "5.º año"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(listReplyData)
      
    elif "1.º año" in text:
        text = "*Horarios Primer Año*:\nhttps://docs.google.com/spreadsheets/d/1F5a7XU02qxdlo-Ejk7JzJSEKSiCbidQs/edit#gid=372359609"
        
        list.append(text_message(number,text))
        
    elif "2.º año" in text:
        text = "*Horarios Segundo Año*:\nhttps://docs.google.com/spreadsheets/d/17nAIjV29lJGfbQbqG0eCX-dHpn-MKRBN/edit#gid=418492156"
        list.append(text_message(number,text))
        
        text = "*Electivas Segundo Año*:\nhttps://docs.google.com/spreadsheets/d/1vG_qQwl366P2kRWUr1tScy99xvVsxt-L/edit?rtpof=true&sd=true#gid=1430635041"
        list.append(text_message(number,text))
    
    elif "3.º año" in text:
        text = "*Horarios Tercer Año*:\nhttps://docs.google.com/spreadsheets/d/1v_-DEmZM6v3e_DOqDH_KmBpmsboNU2Xu/edit?usp=share_link&ouid=112405360630548424739&rtpof=true&sd=true"
        list.append(text_message(number,text))
        
        text = "*Electivas Tercer Año*:\nhttps://docs.google.com/spreadsheets/d/1LOA6lX3pBoSIPR_T4nOEE5wnVyrNbA2G/edit?rtpof=true&sd=true#gid=611337920"
        list.append(text_message(number,text))
    
    elif "4.º año" in text:
        text = "*Horarios Cuarto Año*:\nhttps://docs.google.com/spreadsheets/d/1arpNIGkjwgJ96e1OM0CiHJkNjwphvYCz/edit?rtpof=true&sd=true"
        list.append(text_message(number,text))
        
        text = "*Electivas Cuarto Año*:\nhttps://docs.google.com/spreadsheets/d/1arpNIGkjwgJ96e1OM0CiHJkNjwphvYCz/edit?rtpof=true&sd=true#gid=1473163369"
        list.append(text_message(number,text))
    
    elif "5.º año" in text:
        text = "*Horarios Cuarto Año*:\nhttps://docs.google.com/spreadsheets/d/15U7ZblxXeVqzLUMd0NAQic8kFxB6oW0P/edit#gid=1519933296"
        list.append(text_message(number,text))
        
        text = "*Electivas Segundo Año*:\nhttps://docs.google.com/spreadsheets/d/14EaFHnbqcDu8WZu1gqy0lQ9FbbAFUypf/edit#gid=36529863"
        list.append(text_message(number,text))

    elif "como llego?" in text:
        longitude = '-32.9544144'
        latitude = '-60.6436580'
        location_name = "UTN Rosario"
        adress = "2000, Zeballos 1341, S2000 Rosario, Santa Fe"
      
        list.append(send_location(number, longitude, latitude, location_name, adress))
        
    else :
        body = "¡Hola! 👋 Bienvenido a UTN Regional Rosario. Selecciona una opcion para continuar"
        footer = "@UTNRosario"
        options = ["Calendario academico", "Plan de estudios", "Horarios"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)

        list.append(listReplyData)

    for item in list:
        enviar_mensaje_whatsapp(item)
        
        
    
