from decouple import config

token = config('TOKEN')#'bigdateros'

whatsapp_token = config('WHATSAPP_TOKEN')

whatsapp_url = config('WHATSAPP_URL')



esperando_monto = False
esperando_nota = False
ingreso = False
gasto = False

monto = 0
nota = ""