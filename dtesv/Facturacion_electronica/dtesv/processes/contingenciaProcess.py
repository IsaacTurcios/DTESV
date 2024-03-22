import json
import requests
from datetime import datetime, timedelta

from dtesv.models import Documentos ,Emisor,Receptor,DocumentosDetalle,ExtencionEntrega,DocumentosAsociados,Pagos,Parametros,C015Tributos
import dtesv.processes.constructor_dicionario as constructor_dicionario
import dtesv.processes.procesorDocMhLote as procesorLote 
from dtesv.models.documentos import Documentos
from dtesv.models.contingencia import contingencias
from dtesv.models  import Company
import uuid
import os
import pytz

import base64


class Contingencia:
    def process_data_document(request,tipo_contingencia,motivo,fecha_ini,fecha_fin,hora_ini,hora_fin):
         
        
        nombre_empresa = request.session['empresas'][0]
        emisor_id = Company.objects.get(name=nombre_empresa).emisor
        fecha_actual = datetime.now()
        zona_horaria = pytz.timezone('America/El_Salvador')
        fecha_actual_sv = fecha_actual.astimezone(zona_horaria)
        fecha_manana_sv = fecha_actual_sv + timedelta(days=1)
        # Sumar un día a la fecha actual
        #fecha_manana = fecha_actual + timedelta(days=1)
        fecha_formateada = fecha_actual_sv.strftime("%Y-%m-%d")
        hora_formateada = fecha_actual_sv.strftime("%H:%M:%S")

        #documentos = Documentos.objects.filter(fecEmi__lt=fecha_manana,estado="RECHAZADO",en_contingencia=False)
        #documentos = Documentos.objects.filter(en_contingencia=True)

        documentos = Documentos.objects.filter(
                                en_contingencia=True,
                                fecEmi=fecha_ini,
                                horEmi__gt=hora_ini,
                                horEmi__lt=hora_fin,
                                estado = 'Nuevo'
                            )

        if len(documentos)>0:
            guid = uuid.uuid4()
           
            nueva_contingencia = contingencias(version=3,
                                                ambiente=emisor_id.ambiente_trabajo,
                                                codigoGeneracion=guid,
                                                fTransmision=fecha_formateada,
                                                hTransmision=hora_formateada,
                                                emisor_id=emisor_id.id,  # Asigna la ID del emisor
                                                
                                                fInicio=fecha_ini,
                                                fFin=fecha_fin,
                                                hInicio=hora_ini,
                                                hFin=hora_fin,
                                                tipoContingencia_id=tipo_contingencia,  # Asigna la ID del tipo de contingencia
                                                motivoContingencia=motivo,
                                                selloRecepcion=None)
                                                
                           

        # Guarda la nueva contingencia en la base de datos
            nueva_contingencia.save()    
              # Asigna los documentos a la contingencia utilizando el método set
            nueva_contingencia.detalleDTE.set(documentos)
            documentos.update(estado='CONTING', en_contingencia=True,tipoContingencia = tipo_contingencia
                              , tipoModelo = 2 ,tipoTransmision =2, motivoContin = motivo,)

            message = Contingencia.generar_solicitud_mh(request,nueva_contingencia,Company.objects.get(name=nombre_empresa))
        else:
            message ="Nada que procesar"
        return message

    def generar_solicitud_mh(request,contingencia_solicitud,company_id):
        try:
            detalleDTE_values = []
            for index, detDTE in enumerate(contingencia_solicitud.detalleDTE.values()):
                detalleDTE_values.append({'noItem':index+1,'codigoGeneracion':detDTE['codigoGeneracion'],'tipoDoc':detDTE['tipodocumento_id']})

            dic_contingencia = { "identificacion": {
                                            "version": contingencia_solicitud.version,
                                            "ambiente": contingencia_solicitud.ambiente.codigo,
                                            "codigoGeneracion": str(contingencia_solicitud.codigoGeneracion).upper(),
                                            "fTransmision":contingencia_solicitud.fTransmision,
                                            "hTransmision": contingencia_solicitud.hTransmision
                                           # "fTransmision":contingencia_solicitud.fFin.strftime('%Y/%m/%d') if isinstance(contingencia_solicitud.fFin, datetime) else contingencia_solicitud.fFin,
                                           # "fTransmision":contingencia_solicitud.fFin.strftime('%Y/%m/%d') if isinstance(contingencia_solicitud.fFin, datetime) else contingencia_solicitud.fFin,
                                            #"hTransmision": contingencia_solicitud.hTransmision.strftime('%H:%M:%S') if isinstance(contingencia_solicitud.hTransmision, datetime) else contingencia_solicitud.hTransmision,
                                        },
                                        "emisor": {
                                            "nit": contingencia_solicitud.emisor.nit,
                                            "nombre": contingencia_solicitud.emisor.nombre,
                                            "nombreResponsable": contingencia_solicitud.emisor.nombre,
                                            "tipoDocResponsable": "36",
                                            "numeroDocResponsable": contingencia_solicitud.emisor.nit,
                                            "tipoEstablecimiento": "01",
                                            "codEstableMH": None,
                                            "codPuntoVenta": None,
                                            "telefono": contingencia_solicitud.emisor.telefono,
                                            "correo": contingencia_solicitud.emisor.correo
                                        },
                                        "detalleDTE": detalleDTE_values,
                                        "motivo": {
                                            
                                            "fInicio": contingencia_solicitud.fInicio.strftime('%Y/%m/%d') if isinstance(contingencia_solicitud.fInicio, datetime) else contingencia_solicitud.fInicio ,                                            
                                            "fFin": contingencia_solicitud.fFin.strftime('%Y/%m/%d') if isinstance(contingencia_solicitud.fFin, datetime) else contingencia_solicitud.fFin,
                                            "hInicio": contingencia_solicitud.hInicio.strftime('%H:%M:%S') if isinstance(contingencia_solicitud.hInicio, datetime) else contingencia_solicitud.hInicio + ':00',                                            
                                            "hFin":contingencia_solicitud.hFin.strftime('%H:%M:%S') if isinstance(contingencia_solicitud.hFin, datetime) else contingencia_solicitud.hFin  + ':00',
                                            "tipoContingencia": int(contingencia_solicitud.tipoContingencia.codigo),
                                            "motivoContingencia": contingencia_solicitud.motivoContingencia
                                        }
                                    }
            
            result_mh = constructor_dicionario.DocumentoDiccionarioStruc.envio_contingencia_mh(dic_contingencia,company_id)
            
            contingencia_solicitud.estado = result_mh[0]['estado']
            if result_mh[0]['estado'] == 'RECIBIDO':
                contingencia_solicitud.selloRecepcion =  result_mh[0]['selloRecibido']
                contingencia_solicitud.observaciones_mh = result_mh[0]['mensaje']+' '+ str(result_mh[0]['observaciones'])
                for documento in contingencia_solicitud.detalleDTE.all():
                    documento.estado = 'RECIBIDO'
                    documento.save()
                    contingencia_solicitud.save()
                Contingencia.procesar_documentos_lote(None,request,contingencia_solicitud.detalleDTE.all())    
            else :
                contingencia_solicitud.selloRecepcion =  result_mh[0]['selloRecibido']                
                contingencia_solicitud.observaciones_mh = result_mh[0]['mensaje']+' '+ str(result_mh[0]['observaciones'])
                contingencia_solicitud.save()
            
            return (contingencia_solicitud.observaciones_mh)
        except Exception as e:
            print(str(e))
            return ('Error')
       




    def procesar_documentos_lote(self,company,documentos):
       doclote =  procesorLote.procesorLote.get_documentos_lote(self,company,documentos)


    def enviar_solicitud(codigoGeneracion,empresa_id):
        empresaId = empresa_id
        documento = contingencias.objects.get(codigoGeneracion=codigoGeneracion)
        company =  Company.objects.get(id=empresaId)

        Contingencia.generar_solicitud_mh(documento,company)
