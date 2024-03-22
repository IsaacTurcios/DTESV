# En tu vista Django
from django.views import View
from django.http import JsonResponse
from dtesv.processes.contingenciaProcess import Contingencia
#from dtesv.tasks import send_emails_for_pending_documents,sell_hellos,procesar_documentos



class ProcessDataViewContin(View):
    def post(self, request, *args, **kwargs):
        try:
            # Llama a la función que ejecuta el procesador
            codigoGeneracion =  kwargs['codigoGeneracion']
            empresa_id = kwargs['empresa_id']
            #result = run_processor(codigoGeneracion)
            
            result = Contingencia.enviar_solicitud(codigoGeneracion,empresa_id)
           # if 'estado' in  result:
           #     if result['estado'] == 'PROCESADO':
           #         result_mail = send_emails_for_pending_documents.delay(codigoGeneracion)
                    

                
            #result = send_emails_for_pending_documents.delay('dos','trs','params')
            #result = sell_hellos.delay('hola hey!!')
            return JsonResponse({'success': True, 'message': str(result)})    
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    