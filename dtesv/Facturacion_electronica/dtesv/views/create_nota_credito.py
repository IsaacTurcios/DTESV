# En tu vista Django
from django.views import View
from django.http import JsonResponse
from dtesv.processes.procesor_runner import run_processor,MainProcessor
from dtesv.models import Documentos,DocumentosDetalle,C002TipoDocumento,C016CondicionOperacion,C025BienesRemitidosTitulos, C015Tributos,Parametros,Company
from dtesv.tasks import send_emails_for_pending_documents,sell_hellos,procesar_documentos
from django.forms.models import model_to_dict
import uuid
import requests
from datetime import datetime,timedelta,date
from dtesv.Apis import consecutivos
import logging
import traceback


logger = logging.getLogger('celery')


class GenerateNotaCredito(View):
    def post(self, request, *args, **kwargs):
        try:
            # Llama a la función que ejecuta el procesador

            company_id = Company.objects.filter(users=request.user).first()
            parametro = company_id.parametros_company_id.first()
            codigoGeneracion =  kwargs['codigoGeneracion']

            documentos = Documentos.objects.filter(codigoGeneracion=codigoGeneracion,en_contingencia=False).first()

            Nota_credito = Documentos.objects.filter(numeroDocumento_rel_guid=codigoGeneracion).first()
            
            
            if documentos and not Nota_credito:
                
                fecha_actuals = datetime.now().date()
                diferencia = fecha_actuals - documentos.fecEmi
                if diferencia < timedelta(days=90):
                    guid = str(uuid.uuid4()).upper()           
                    documento_dict = model_to_dict(documentos)
                    documento_dict['codigoGeneracion'] = guid
                    
                    detalles_lista = [model_to_dict(detalle) for detalle in documentos.documento_detalle_codigoGeneracion_id.all()]
                    DTE_cosecutivo = ''
                        
                    try:   
                        fecha_actual = datetime.now().strftime('%Y-%m-%d')  
                        Nconsecutivos =  consecutivos.ConsecutivosSF('05',parametro).get()
                        if Nconsecutivos:
                                    nuevo_consecutivo = {'sig_consec':'{:015}'.format(int(Nconsecutivos['datos']))}
                                    
                                    
                                # Obtiene los datos en formato JSON
                                   

                                # Imprime los valores retornados por el API

                                    consegutivo = Nconsecutivos['datos']
                                    documento_dict['numeroDocumento_rel_guid'] = documentos.codigoGeneracion
                                    documento_dict['numeroDocumento_rel_corr'] = guid
                                    DTE_cosecutivo = 'DTE-05-M0010000-'+consegutivo
                                    documento_dict['selloRecibido'] =''
                                    documento_dict['tipodocumento'] =C002TipoDocumento.objects.get(codigo='05')
                                    documento_dict['clase_documento'] ='D'
                                    documento_dict['fecEmi'] =fecha_actual
                                    documento_dict['num_documento'] =consegutivo
                                    documento_dict['estado'] ='Nuevo'
                                    documento_dict['numeroControl'] =DTE_cosecutivo
                                    documento_dict['codigoGeneracion'] =guid
                                    documento_dict['observaciones_mh'] =None
                                    documento_dict['observacion_proceso'] ='Nota de Credito que Anula al Documento:'+documentos.codigoGeneracion+', Con numero ERP:'+documentos.num_documento
                                    documento_dict['condicionOperacion'] =documentos.condicionOperacion
                                    documento_dict['codigo_iva'] =documentos.codigo_iva
                                    documento_dict['bienTitulo'] =C025BienesRemitidosTitulos.objects.get(codigo='01')
                                    documento_dict['receptor_id'] =documentos.receptor_id
                                    documento_dict['emisor_id'] =documentos.emisor_id
                                    documento_dict['receptor_origen'] =documentos.receptor_origen if documentos.receptor_origen else documentos.receptor_id
                                    documento_dict['tipoModelo'] =documentos.tipoModelo
                                    documento_dict['tipoOperacion'] =documentos.tipoOperacion
                                    documento_dict['fecha_anula_mh'] =None
                                    documento_dict['rutaEntrega'] ='ECXC'
                                    documento_dict['codigoGenInvalida'] =None
                                    documento_dict['montoTotalOperacion'] =documentos.totalPagar

                                     
                                    
                                    
                                    

                                    nuevo_documento = Documentos(**documento_dict)   
                                    nuevo_documento.save()

                                    for detalle_dict in detalles_lista:
                                        # Asegurarse de establecer la relación con el nuevo documento
                                        detalle_dict['codigoGeneracion_id'] = nuevo_documento
                                        detalle_dict['numeroDocumento'] = documentos.codigoGeneracion
                                        detalle_dict['codTributo'] = C015Tributos.objects.get(codigo='20')
                                        # Crear un nuevo objeto DocumentosDetalle y guardarlo en la base de datos
                                        nuevo_detalle = DocumentosDetalle(**detalle_dict)
                                        nuevo_detalle.save()
                                    


                                    
                                    documentos.estado = 'ANULADONC'
                                    documentos.anuladoErp = False
                                    documentos.observacion_proceso = 'Anulado con NC Local No.:'+nuevo_documento.codigoGeneracion+',Nota: Este Documento No Existira en SF'

                                    
                                    documentos.save()
                                    actualizado = consecutivos.ConsecutivosSF(['05',nuevo_consecutivo],parametro).set()

                                    result = 'OK'
                    except Exception as er:
                        for ar in er.args:
                            result = ar
                            logger.error(f"Error in create NC: {result}", exc_info=True)
                            traceback.print_exc()
                else:
                    result = 'No se puede Realizar Nota de Credito a Documento con mas de 90 Dias de Generado'
                    logger.error(f"Error in create NC: {result}", exc_info=True)
                    traceback.print_exc()
                    
                    
               #lineas =  documentos.documento_detalle_codigoGeneracion_id.all()
            else:
                 result = 'Documento ya cuenta con  Nota de Credito para Anulacion'   
                 logger.error(f"Error in create NC: {result}", exc_info=True)
                 traceback.print_exc()


            #result = run_processor(codigoGeneracion)
            
            #result = MainProcessor( codigoGeneracion).run()
           # result = procesar_documentos.delay(codigoGeneracion)
           # if 'estado' in  result:
           #     if result['estado'] == 'PROCESADO':
           #         result_mail = send_emails_for_pending_documents.delay(codigoGeneracion)
                    
           
                
            #result = send_emails_for_pending_documents.delay('dos','trs','params')
            #result = sell_hellos.delay('hola hey!!')
            return JsonResponse({'success': True, 'message': str(result)})    
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})