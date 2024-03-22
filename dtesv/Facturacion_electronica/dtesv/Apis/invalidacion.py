
import requests
import json
from requests.exceptions import Timeout,RequestException 
 

# Este metodo envia la Firma y la informacion requerida  a hacienda y retorna el resultado dado por mh

class post_recepciondte ():
    def __init__(self,args,parametros):
         
        self.args = args
        self.parametros = parametros
    def sent_data(self):      
        TIMEOUT = 50
        try:
            auth = self.args['auth']   
            documento = self.args['docuemnto']  
            API_ENDPOINT = self.parametros.url_invalidacion
            response = requests.post(API_ENDPOINT,json=documento,timeout=TIMEOUT,headers={'content-type': 'application/json','Authorization':auth})
            result_js = response.json()
        except RequestException as er:
            for ar in er.args:
              if 'No connection' in str(ar) : 
                    respuesta_mh = ({'status':'RECHAZADO','descripcionMsg':" Error en conexion a endpoint "+API_ENDPOINT ,'observaciones':"endpoint  fuera de linea o sin  acceso a internet",'selloRecibido':None})   
                    result_js = respuesta_mh
        return result_js