from dtesv.models import Documentos ,DocumentosDetalle,ExtencionEntrega,DocumentosAsociados,Pagos
from django.http import FileResponse, HttpResponse, JsonResponse
import dtesv.Apis.envio_email_dm as enviar_email
from dtesv.models import User,Company,Documentos
#from dtesv.processes.procesorDocMh import MainProcessor
from django.http import HttpRequest
import os



def sent_email(request, codigoGeneracion):
        if isinstance(request, HttpRequest):
            company_id = Company.objects.filter(users=request.user).first()
            parametro = company_id.parametros_company_id.first()
        else:
            parametro = request
            company_id = parametro.company_id
        
        ruta_pdf = parametro.attachment_files_path+codigoGeneracion+'.pdf'
        ruta_json = parametro.attachment_files_path+codigoGeneracion+'.json'
        if company_id:
            if os.path.isfile(ruta_pdf) and  os.path.isfile(ruta_json):
                documento = Documentos.objects.filter(emisor_id=company_id.emisor_id, codigoGeneracion=codigoGeneracion).first()
                if documento:
                        dic_sent={"mail" :documento.receptor_origen.correo if documento.receptor_origen else documento.receptor_id.correo if documento.receptor_id 
                                  else documento.proveedor_id.correo if documento.proveedor_id else 'efactura@lamorazan.com' , 
                            #"mail" : 'carlos_hercules@lamorazan.com', 
                                "file_name" : codigoGeneracion,
                                #"pathfile" : parametro.attachment_email_path,
                                "pathfile" : '/mnt/h',
                                "doc_number" : documento.selloRecibido,
                                "customer_name" : documento.receptor_id.nombre if documento.receptor_id else documento.proveedor_id.nombre ,
                                "customer_code" : documento.receptor_id.pk if documento.receptor_id else documento.proveedor_id.codigo,
                                "date" : str(documento.fecEmi),
                                "doc_type" : documento.tipodocumento.valor + '-ANULADO' if documento.estado=='INVALIDADO' else documento.tipodocumento.valor  ,
                                "amount" : documento.totalPagar,
                                "notice" : "Aprovecha nuestra promociones"
                            
                        }
                        message = enviar_email.sentEmail(dic_sent,parametro).sent()
                    
            else :
               message = "No Existen Los Archivo pdf y json"
              # result =  MainProcessor(request,codigoGeneracion).run_email_worker()
        return JsonResponse({'result': message}, status=404)