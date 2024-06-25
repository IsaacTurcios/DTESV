from celery import shared_task , Task
from dtesv.models import Documentos , Parametros , Company
import dtesv.processes.create_pdf as gen_pdf
import dtesv.processes.procesorDocMh as  DataProcessor
import dtesv.processes.create_json as gen_json
import dtesv.processes.invalidDocumento as invelid_doc
import os
import dtesv.views.sent_email as enviar_email
import dtesv.views.sent_email_django as mail_sent
import traceback
import redis
import logging

import json

logger = logging.getLogger('celery')

#@shared_task(queue='general_tasks')
@shared_task(queue='default')
def send_emails_for_pending_documents(codigoGeneracion):
   
      try:    

            document = Documentos.objects.get(codigoGeneracion=codigoGeneracion)
            mi_compania = Company.objects.get(id=1)  # Ajusta el ID según tus necesidades

            # Obtén los parámetros asociados a la compañía
            parametros = Parametros.objects.get(company_id=mi_compania)            
            ruta_pdf_file = gen_pdf.gen_pdf.generarPdf(document,codigoGeneracion)
            if os.path.isfile(ruta_pdf_file['pdf_file']): 
                  #result_mail = enviar_email.sent_email(parametros,codigoGeneracion)
                  result_mail = mail_sent.enviar_correo(parametros,codigoGeneracion)

                  estadoml = json.loads(result_mail.content)['result']
                  #estadoml = 'Enviado!'
                  
                  if    estadoml == 'Enviado!':
                        
                        document.email_enviado = True
                        
                        document.save()
                        logger.info(estadoml,exc_info=True)
                        traceback.print_exc()
                        #estado = print(f'Correo enviado para {codigoGeneracion}. Estado: {estadoml}')
                         
                  else :
                        document.observacion_proceso = estadoml
                        logger.info(estadoml,exc_info=True)
                        traceback.print_exc()
                         
            return estadoml
      except Exception as e:
        logger.error(f"Error in send_emails_for_pending_documents: {e}", exc_info=True)
        traceback.print_exc()
        return f"Error in send_emails_for_pending_documents: {e}"



#@shared_task(queue='general_tasks')
@shared_task(queue='urgent')
def procesar_documentos(codigoGen):
    try:
       
        
        result_proces = DataProcessor.DataProcessor.process_data_document(None,codigoGen)
        
        if len(result_proces) > 0:
            documento_procesado = result_proces[0]
            estado = documento_procesado.get('estado')
            result = documento_procesado.get('result')

            if (estado not in ['RECHAZADO','ERROR'] and estado is not None) or \
               (result is not None and 'Error' not in result):
                logger.info(str(documento_procesado),exc_info=True)
                dicto_json = documento_procesado['dic_dte']
                dicto_json['identificacion']['selloRecibido'] = documento_procesado['selloRecibido']
                gen_json.gen_json.create_fileJson(None, dicto_json)
                send_emails_for_pending_documents.delay(codigoGen)
                resultado = documento_procesado['selloRecibido']
            else:
                resultado = estado
            return resultado

    except Exception as e:
        # Agrega manejo de excepciones y registra el error
        logger.error(f"Error en procesar_documentos: {e}", exc_info=True)
        resultado = f"Error en procesar_documentos: {e}"
        return resultado

    


@shared_task()
def sell_hellos(parametros):
    print(parametros)
     
      
def test_redis_connection(host, port):
    try:
        print(f"Probando conexión a Redis en {host}:{port}")
        redis_connection = redis.StrictRedis(host=host, port=port, decode_responses=True)
        redis_connection.ping()  # Intenta realizar un ping a Redis
        print("Conexión a Redis exitosa")
        redis_connection.close()

    except Exception as e:
        print(f"No se pudo conectar a Redis. Error: {e}")
        traceback.print_exc()


@shared_task(queue='default')
def invalidacion_documento(invalid_doc):
    try:
        invalid_data =  invelid_doc.InvalidProcessor.invalid_document(None,invalid_doc)
        document = invalid_data['documento'] if 'documento' in invalid_data else None

        if document:
            if document.estado == 'INVALIDADO':            
            #doucmento = constructor_dicionario.DocumentoDiccionarioStruc.get_diccionario(invalid_doc['documento']['codigoGeneracion'])  
                if document:        
                    gen_json.gen_json.write_fileJSon(None, document)
                    #send_emails_for_pending_documents.delay(document.codigoGeneracion)  
                return document.selloInvalidacion if document.selloInvalidacion  else 'INVALIDADO'

    except Exception as e:
        # Agrega manejo de excepciones y registra el error
        logger.error(f"Error en invalidacion_documento: {e}", exc_info=True)
        return f"Error en invalidacion_documento: {e}"
