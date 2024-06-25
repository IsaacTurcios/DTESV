# dtesv/views.py (o cualquier otro archivo desde donde desees enviar el correo)

from dtesv.utilities.email_utils import enviar_correo_con_adjuntos
from dtesv.models import User,Company,Documentos
from django.http import HttpRequest,JsonResponse
import os
from django.template.loader import render_to_string

def enviar_correo(request,codigoGeneracion):
    documento = Documentos.objects.filter(codigoGeneracion=codigoGeneracion).first()
    if isinstance(request, HttpRequest):
            company_id = Company.objects.filter(users=request.user).first()
            parametro = company_id.parametros_company_id.first()
    else:
           parametro =request
           company_id = documento.emisor_id.company
    
    ruta_pdf = parametro.attachment_files_path+codigoGeneracion+'.pdf'
    ruta_json = parametro.attachment_files_path+codigoGeneracion+'.json'

    subject = 'Factura Electronica'+ ' '+ documento.codigoGeneracion
    
    recipient_list = ['iturcios@sistecsv.com']

    attachments = []
    if os.path.isfile(ruta_pdf) and  os.path.isfile(ruta_json):
        with open(ruta_pdf, 'rb') as f:
            attachments.append({
                'filename': codigoGeneracion+'.pdf',
                'content': f.read(),
                'mimetype': 'application/pdf'
            })

        with open(ruta_json, 'rb') as f:
            attachments.append({
                'filename': codigoGeneracion+'.json',
                'content': f.read(),
            'mimetype': 'application/json'
            })


         # Crear el mensaje HTML utilizando una plantilla
        context = {
            'cliente': documento.receptor_id.nombre,  # o cualquier información del cliente
            'documento': documento,
            'company': company_id
        }
        html_message  = render_to_string('email_template.html', context)

        retorno = enviar_correo_con_adjuntos(subject, '', recipient_list, attachments, html_message=html_message)
        if retorno ==1 :
            message = 'Correo Enviado'
        else :
            message = 'No se pudo enviar Correo'
    else:
            message = "No Existen Los Archivo pdf y json"

    return JsonResponse({'result': message}, status=200 if retorno == 1 else 404)