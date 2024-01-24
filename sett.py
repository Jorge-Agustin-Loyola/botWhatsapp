from decouple import config

token = config('TOKEN')#'bigdateros'

whatsapp_token = str(config('WHATSAPP_TOKEN'))

whatsapp_url = str(config('WHATSAPP_URL'))



esperando_monto = False
esperando_nota = False
ingreso = False
gasto = False

monto = 0
nota = ""