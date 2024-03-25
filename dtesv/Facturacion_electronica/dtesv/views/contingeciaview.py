from django.views import View
from django.http import JsonResponse

from dtesv.processes.contingenciaProcess import Contingencia

class ContingenciaView(View):
    def post(self, request, *args, **kwargs):
        print(request)
        
        response = Contingencia.process_data_document(request,kwargs['tipo_contingencia'],kwargs['motivo'],kwargs['fecha_inicio'],kwargs['fecha_fin'],
                                                      kwargs['hora_ini'],kwargs['hora_fin'])
         
        return JsonResponse({'message': str(response[0])})