from django.views import View
from django.http import JsonResponse

from dtesv.models import Documentos

class receptor_from_document(View):
    def post(self, request, *args, **kwargs):
        
       # response =   Documentos.objects.filter(codigoGeneracion = kwargs['codigoGeneracion']).get()
         

       # if response: 
       #     return  JsonResponse({'message': response.receptor_origen_id if response.receptor_origen_id else response.receptor_id_id })        
            
       # return None
        
        id_result = ''
        response =   Documentos.objects.filter(codigoGeneracion = kwargs['codigoGeneracion']).get()
        if response.tipodocumento.codigo in ['07','14']:
           id_result = response.proveedor_id.codigo
        else:
            id_result = response.receptor_origen.codigo if response.receptor_origen else response.receptor_id.codigo
        if response: 
            return  JsonResponse({'message': id_result})        
            
        return None
    
