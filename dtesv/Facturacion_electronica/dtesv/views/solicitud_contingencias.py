import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from dtesv.models import User,Company,Documentos,Parametros,contingencias
from datetime import datetime

def solicitud_contingencias_view(request):
     
    return render(request, 'contingencias.html')


def data_contingencias(request,fecha_desde,fecha_hasta,empresa_id):
    es_admin = request.user.is_superuser
    fecha_desde_d = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
    fecha_hasta_d = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
    print(fecha_desde)
    company_id = Company.objects.filter(id=empresa_id).first()
    if company_id:
        documentos = contingencias.objects.filter(
    emisor=company_id.emisor_id,
    fTransmision__gte=fecha_desde_d,
        fTransmision__lte=fecha_hasta_d,
                    ).values(
                        'codigoGeneracion',
                        'tipoContingencia__valor',  # Corregir el nombre del campo para obtener el ID de tipoContingencia
                        'estado',
                        'fTransmision',
                        'hTransmision',
                        'fInicio',
                        'fFin',
                        'hInicio',
                        'hFin',
                        'motivoContingencia',
                        'selloRecepcion',
                        'ambiente',
                        'observacion_proceso',
                        'observaciones_mh',
                    )
    else:
        documentos = []
    
    documentos_con_fechas_formateadas = [
    {
        'codigoGeneracion': documento['codigoGeneracion'],
        'tipoContingencia': documento['tipoContingencia__valor'],
        'estado': documento['estado'],
        'fTransmision': documento['fTransmision'].strftime('%d/%m/%Y') if documento['fTransmision'] else None,
        'hTransmision': documento['hTransmision'],
        'fInicio': documento['fInicio'].strftime('%d/%m/%Y') if documento['fInicio'] else None,  
        'hInicio': documento['hInicio'],
        'fFin': documento['fFin'].strftime('%d/%m/%Y') if documento['fFin'] else None,
        'hFin': documento['hFin'],        
        'motivoContingencia': documento['motivoContingencia'],        
        'selloRecepcion': documento['selloRecepcion'],
        'observaciones_mh': documento['observaciones_mh'],         
        'observacion_proceso': documento['observacion_proceso'],
        'ambiente': documento['ambiente'],
        
    }
    for documento in documentos
        ]
    context = {
        'documentos': documentos_con_fechas_formateadas,
        'es_admin': es_admin,
    }
    return render(request, 'contingencias.html', context)