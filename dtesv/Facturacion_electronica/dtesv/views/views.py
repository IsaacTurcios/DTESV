from .home_view import CustomLoginView ,profile_view,home,documentos_by_fecha,obtener_datos_documento ,documentos,tipo_contingencia
from .process_view import ProcessDataView
from .re_process_view import ReProcessDataView
from .generar_pdf import ger_pdf
from .dashboard import dashboard_view,dashboard_data_view,url_status,url_status_data
from .rest_api import (
    ReceptorDetail,
    DocumentosCreateAPIView,
    DocumentosRetrieveAPIView,
    DocumentosUpdateCompleteAPIView,
    InvalidacionClass,
    DocumentoClienteTelefono,
    DocumentoCliente,
    DocumentosLoteCreateAPIView,
    CustomObtainAuthToken,
    ProveedorDetail,
     DownloadFilesAPI
)
from .sent_email import sent_email
from .edicion_receptor import edit_receptor
from .municipio_emisor import get_municipios_by_departamento

from . contingeciaview import ContingenciaView
from . get_receptor_from_dte import receptor_from_document
from . update_documentLote import ProcessLoteDocument
from  . solicitud_contingencias import solicitud_contingencias_view,data_contingencias
from . process_contingencia_view import ProcessDataViewContin
from . process_doc_lote_contig import ProcessLoteDocumentConting
from . create_nota_credito import GenerateNotaCredito
from . GenerarPDFMasivo import GenerarPDFS
from . edit_documento import edit_Documento
# siendo el archivo view  la vista principal llamo las otras vistas  y las asigno a variables que seran llamadas desde las url
CustomLoginViews = CustomLoginView
profile_views = profile_view
homes =home
documento_fecha =documentos_by_fecha
documentoss = documentos
obtener_datos_documentos = obtener_datos_documento
procesoDatos =ProcessDataView
reprocesoDatos = ReProcessDataView
Generar_pdf = ger_pdf.generarPdf
ProcessLoteDocumentContings = ProcessLoteDocumentConting.get
#Settings_list = settings_list
#Settings_create = settings_create
#Settings_edit = settings_edit
#Settings_delete = settings_delete
Dashboard_view = dashboard_view
Dashboard_data_view =dashboard_data_view
solicitud_contingencias_views = solicitud_contingencias_view
data_contingencias_views = data_contingencias
procesar_contingencia = ProcessDataViewContin
ReceptorDetails = ReceptorDetail
ProveedorDetails = ProveedorDetail
DocumentosCreateAPIViews = DocumentosCreateAPIView
DocumentosRetrieveAPIViews = DocumentosRetrieveAPIView
DocumentosUpdateCompleteAPIViews = DocumentosUpdateCompleteAPIView
sentEmail = sent_email
invalidarDocumento = InvalidacionClass
tipo_contingecias =tipo_contingencia
contingencia = ContingenciaView
DocumentoClienteTelefonos =DocumentoClienteTelefono
DocumentoClientes =DocumentoCliente
receptor_from_documents = receptor_from_document
urls_status =url_status
edit_receptors =edit_receptor
DocumentosLoteCreateAPIViews =DocumentosLoteCreateAPIView
ProcessLoteDocuments = ProcessLoteDocument
edit_Documentos = edit_Documento
DownloadFilesAPIs = DownloadFilesAPI
GenerateNotaCreditos = GenerateNotaCredito
get_municipios_by_departamentos = get_municipios_by_departamento