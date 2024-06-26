import json
import requests
from datetime import datetime

from dtesv.models import Documentos ,Emisor,Receptor,DocumentosDetalle,ExtencionEntrega,DocumentosAsociados,Pagos,Parametros,C015Tributos,Company
import dtesv.processes.validate_schema as  validateSchema
import dtesv.processes.create_pdf as  gen_pdf
import dtesv.processes.create_json as  gen_json
import dtesv.Apis.firmador as firmador
import dtesv.Apis.autentificador as autenticador
import dtesv.Apis.invalidacion as mh_invalidacion
import dtesv.views.sent_email as enviar_email
import dtesv.processes.constructor_dicionario as get_dic_documento
import os
import pytz

import base64


class InvalidProcessor:
    def invalid_document(self,invalid_doc):
        result = ''
        fecha_actual = datetime.now()
        fecha_actual_str = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
        company_ids = Company.objects.filter(emisor__nombre=invalid_doc['emisor']['nombre']).values_list('id', flat=True)

        parametros = Parametros.objects.filter(company_id = company_ids[0]).first()
        emisor_data =Emisor.objects.filter(nit = invalid_doc['emisor']['nit']).first() 
        documentos = Documentos.objects.filter(emisor_id=emisor_data.id, codigoGeneracion=invalid_doc['documento']['codigoGeneracion']).first() 
        if documentos.estado == 'PROCESADO' and documentos.selloRecibido:
            validacion_schema =  validateSchema.schemaValidate({'tipo':'anulacion-schema-v2','json':invalid_doc}).validar_schema()
            if  validacion_schema == True:
                dic_datos_dte = ({ 'nit':emisor_data.nit,'activo':emisor_data.activo,'passwordPri':base64.b64decode(emisor_data.passwordpri).decode("utf-16") , 'dteJson':invalid_doc})
                dic_otra_info = ({'ambiente':invalid_doc['identificacion']['ambiente'],'version':invalid_doc['identificacion']['version'],'tipoDte':invalid_doc['documento']['tipoDte'],'pwd':base64.b64decode(emisor_data.mh_auth).decode("utf-16")})    
                gen_json.gen_json.save_fileJSon(None,dic_datos_dte) 
               # nombre_archivo = invalid_doc['documento']['codigoGeneracion']+'.json'
               # mi_json = json.dumps(dic_datos_dte)
               # with open(nombre_archivo, 'w') as archivo:
               #     archivo.write(mi_json)

                result_firma = firmador.get_dte_firma(dic_datos_dte,parametros).get_firma()
                if result_firma['status'] != 'OK':
                    result = result_firma
                else:
                    uth_data = ({'user':emisor_data.nit,'pwd':dic_otra_info['pwd']})
                    token = autenticador.authenticate(uth_data,parametros).get_token()  
                    if token['status'] == 'OK':
                            dic_to_repcion_mh = ({'ambiente':dic_otra_info['ambiente'],'idEnvio': 1117,'version': int(dic_otra_info['version']),'tipoDte': dic_otra_info['tipoDte'],'documento':result_firma['body']})
                            dic_process = ({'auth':token['body']['token'],'docuemnto':dic_to_repcion_mh})
                            respuesta_dte_mh = mh_invalidacion.post_recepciondte(dic_process,parametros).sent_data()

                            if respuesta_dte_mh['estado'] == 'RECHAZADO':                                
                                cadena = documentos.observaciones_mh if documentos.observaciones_mh else "."
                                mensaje_mh = respuesta_dte_mh['descripcionMsg'] if respuesta_dte_mh['descripcionMsg'] else "."
                                if isinstance(respuesta_dte_mh['observaciones'], list) and len(respuesta_dte_mh['observaciones']) >0:
                                    
                                    cadena =  fecha_actual_str +':'+mensaje_mh+"-"+(','.join(respuesta_dte_mh['observaciones']))+','+cadena
                                else:
                                    cadena = fecha_actual_str + ':'+respuesta_dte_mh['descripcionMsg'] +','+cadena
                                result = respuesta_dte_mh
                                data_update ={'tipo':'mh_error','estado':respuesta_dte_mh['estado'],'cadena':cadena}
                                InvalidProcessor.update_documento(self,documentos,data_update)
                            else:
                                data_update ={'tipo':'mh_log','estado':'PROCESADO','cadena':respuesta_dte_mh,
                                              'motivoAnulacion': invalid_doc['motivo']['motivoAnulacion']} 
                                
                                document_up = InvalidProcessor.update_documento(self,documentos,data_update)
                                respuesta_dte_mh ['documento'] = document_up
                                result = respuesta_dte_mh
            else:
                result = {'message':validacion_schema,}      
                historico = documentos.observacion_proceso
                if historico:
                    
                    result = {"message": fecha_actual_str+':' +'validacion_schema:'+validacion_schema +','+ historico,'codigoGeneracion':invalid_doc['documento']['codigoGeneracion']}
                else:
                    result =  {"message":fecha_actual_str+':' +'validacion_schema:'+validacion_schema ,'codigoGeneracion':invalid_doc['documento']['codigoGeneracion']}
                data_update ={'tipo':'validacion_schema','estado':'ERROR','cadena':'validacion_schema: ' + validacion_schema}
                #self.update_documento(documentos,data_update)
                document_up = InvalidProcessor.update_documento(self,documentos,data_update)  


        return result

    def update_documento(self,document,result):
        fecha_actual = datetime.now()            
        zona_horaria = pytz.timezone('America/El_Salvador')
        fecha_actual_sv = fecha_actual.astimezone(zona_horaria)
        document.estado_anulado =  result['estado']        
        if result['tipo'] == 'mh_log':
            if result['cadena']['selloRecibido']:
                document.selloInvalidacion =  result['cadena']['selloRecibido']
                document.observaciones_mh =result['cadena']['descripcionMsg'] + (','.join(result['cadena']['codigoGeneracion'])) if result['cadena']['observaciones'] else "."
                document.estado = 'INVALIDADO'
                document.motivoInvalidacion = result['motivoAnulacion']
                document.codigoGenInvalida = result['cadena']['codigoGeneracion']
            else:                
                document.observaciones_mh ='INVALIDACION:'+result['cadena']['descripcionMsg'] + (','.join(result['cadena']['codigoGeneracion'])) if result['cadena']['observaciones'] else 'INVALIDACION:' + result['cadena']['descripcionMsg']
        elif  not  result['tipo'] =='validacion_schema':            
            document.observaciones_mh =  result['cadena']
            #document.codigoGenInvalida = result['cadena']['codigoGeneracion']
        else:
            document.observacion_proceso = result['cadena']
            #document.codigoGenInvalida = result['cadena']['codigoGeneracion']
        document.fecha_anula_mh = fecha_actual

        document.save()

        return document

  