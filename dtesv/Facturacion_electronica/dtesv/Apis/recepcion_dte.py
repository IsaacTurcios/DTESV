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
            API_ENDPOINT = self.parametros.url_dte
            response = requests.post(API_ENDPOINT,json=documento,timeout=TIMEOUT,headers={'content-type': 'application/json','Authorization':auth})
            result_js = response.json()
        except RequestException as er:
            for ar in er.args:
              if 'No connection' in str(ar) : 
                    respuesta_mh = ({'status':'RECHAZADO','descripcionMsg':" Error en conexion a endpoint "+API_ENDPOINT ,'observaciones':"endpoint  fuera de linea o sin  acceso a internet",'selloRecibido':None})   
                    result_js = respuesta_mh
        return result_js

class post_recepcioncontingencia ():
    def __init__(self,args,parametros):
         
        self.args = args
        self.parametros = parametros
    def sent_data(self):      
        TIMEOUT = 50
        try:
            auth = self.args['auth']   
            documento = self.args['docuemnto']  
            API_ENDPOINT = self.parametros.url_contingencia
            response = requests.post(API_ENDPOINT,json=documento,timeout=TIMEOUT,headers={'content-type': 'application/json','Authorization':auth})
            result_js = response.json()
        except RequestException as er:
            for ar in er.args:
              if 'No connection' in str(ar) : 
                    respuesta_mh = ({'status':'RECHAZADO','descripcionMsg':" Error en conexion a endpoint "+API_ENDPOINT ,'observaciones':"endpoint  fuera de linea o sin  acceso a internet",'selloRecibido':None})   
                    result_js = respuesta_mh
        return result_js
    

class post_recepciondteLote ():
    def __init__(self,args,parametros):
         
        self.args = args
        self.parametros = parametros
    def sent_data(self):      
        TIMEOUT = 50
        try:
            auth = self.args['auth']   
            documento = self.args['docuemnto']  
            API_ENDPOINT = self.parametros.url_dte_lote
            response = requests.post(API_ENDPOINT,json=documento,timeout=TIMEOUT,headers={'content-type': 'application/json','Authorization':auth})
            result_js = response.json()
        except RequestException as er:
            for ar in er.args:
              if 'No connection' in str(ar) : 
                    respuesta_mh = ({'status':'RECHAZADO','descripcionMsg':" Error en conexion a endpoint "+API_ENDPOINT ,'observaciones':"endpoint  fuera de linea o sin  acceso a internet",'selloRecibido':None})   
                    result_js = respuesta_mh
        return result_js

class get_documentosLote():
    def __init__(self,args,parametros):
         
        self.args = args
        self.parametros = parametros
    def sent_data(self):      
        TIMEOUT = 50
        try:
            auth = self.args['auth']
            loteId = self.args['loteId']
            API_ENDPOINT = self.parametros.url_dte_lote_consulta +loteId
            response = requests.get(API_ENDPOINT,timeout=TIMEOUT,headers={'content-type': 'application/json','Authorization':auth})
            result_js = response.json()
        except RequestException as er:
            for ar in er.args:
              if 'No connection' in str(ar) : 
                    respuesta_mh = ({'status':'RECHAZADO','descripcionMsg':" Error en conexion a endpoint "+API_ENDPOINT ,'observaciones':"endpoint  fuera de linea o sin  acceso a internet",'selloRecibido':None})   
                    result_js = respuesta_mh
        return result_js

class post_consultadte ():
    def __init__(self,args,parametros):
         
        self.args = args
        self.parametros = parametros
    def sent_data(self):      
        TIMEOUT = 50
        try:
            auth = self.args['auth']   
            documento = self.args['docuemnto']  
            API_ENDPOINT = self.parametros.url_dte_consulta
            response = requests.post(API_ENDPOINT,json=documento,timeout=TIMEOUT,headers={'content-type': 'application/json','Authorization':auth})
            result_js = response.json()
        except RequestException as er:
            for ar in er.args:
              if 'No connection' in str(ar) : 
                    respuesta_mh = ({'status':'RECHAZADO','descripcionMsg':" Error en conexion a endpoint "+API_ENDPOINT ,'observaciones':"endpoint  fuera de linea o sin  acceso a internet",'selloRecibido':None})   
                    result_js = respuesta_mh
        return result_js