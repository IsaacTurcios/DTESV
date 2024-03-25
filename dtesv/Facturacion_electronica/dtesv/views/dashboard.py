import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from dtesv.models import User,Company,Documentos,Parametros
from datetime import datetime
 
def dashboard_view(request):
     
    return render(request, 'dashboard.html')

def is_url_online(url):
   
    try:
        response =  requests.head(url)
        if response.status_code == 200:
            return True
        else:
           response = requests.post(url)
           return response.status_code == 200
         
    except requests.exceptions.RequestException:        
            return False
    
def dashboard_data_view(request, filtro):
    company_id = Company.objects.filter(users=request.user).first()
    
   
    
    if company_id:
        documentos = Documentos.objects.filter(emisor_id=company_id.emisor_id)
        if filtro == 'mesActual':
            documentos = documentos.filter(fecEmi__month=datetime.now().month)
        elif filtro == 'anioActual':
            documentos = documentos.filter(fecEmi__year=datetime.now().year)
        
        # Obtener los campos "estado" y "cantidad de documentos"
        documentos_agrupados = documentos.values('estado').annotate(cantidad=Count('codigoGeneracion'))

        # Crear una lista de diccionarios con los datos
        data = []
        for doc in documentos_agrupados:
            data.append({
                'estado': doc['estado'],
                'cantidad': doc['cantidad']
            })

         # Incluir información sobre el estado de la URL en la respuesta JSON
        

    return JsonResponse(data, safe=False)
def url_status(request):
     
    return render(request, 'dashboard.html')
def url_status_data(request, filtro):
    company_id = Company.objects.filter(users=request.user).first()
    parametros = Parametros.objects.first()
    url_keys = {key: value for key, value in parametros.__dict__.items() if 'url' in key}
    url_firmador = parametros.url_firmador
    data = []

    for key, url in url_keys.items():
        if filtro == 'name':
            # Si el filtro es "name", solo retornamos el nombre de la URL
            data.append(key)
        elif filtro == 'state':
            # Si el filtro es "state", retornamos el nombre de la URL y su estado
            result_url = is_url_online(url)
            data.append({'name': key, 'state': result_url})

    return JsonResponse(data, safe=False)