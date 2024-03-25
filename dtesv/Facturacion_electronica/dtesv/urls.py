from django.urls import path
from dtesv.views import views

from django.contrib.auth.views import logout_then_login
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dtesv' 

urlpatterns = [
    path('login/', views.CustomLoginViews.as_view(), name='login'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('home/', views.homes, name='home'),  # Nueva vista después del inicio de sesión
   # path('documentos/', views.documentos, name='documentos'),
    path('documentos/<str:fecha_desde>/<str:fecha_hasta>/<str:empresa_id>/', views.documento_fecha, name='documentos_fecha'),
    path('documentos/<str:codigoGeneracion>/', views.obtener_datos_documento, name='obtener_datos_documento'),
    path('editar_documentos/<str:codigoGeneracion>/', views.edit_Documento, name='editar_documento'),
    path('process_data/<str:codigoGeneracion>/', views.procesoDatos.as_view(), name='process_data'),
    path('crear_nota_credito/<str:codigoGeneracion>/', views.GenerateNotaCredito.as_view(), name='crear_nota_credito'),
    path('generarPDFS/', views.GenerarPDFS, name='generarPDFS'),
    path('reprocess_data/<str:fecha_desde>/<str:fecha_hasta>/', views.reprocesoDatos.as_view(), name='reprocess_data'),
    path('generar_pdf/<str:codigoGeneracion>/', views.ger_pdf.generarPdf, name='generar_pdf'),   
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('contingencias/', views.solicitud_contingencias_view, name='contingencias'),
    path('contingencias/procesaLote/<str:codigoGeneracion>/', views.ProcessLoteDocumentConting.as_view(), name='contin_lote_process'),
    path('contingencias/<str:fecha_desde>/<str:fecha_hasta>/<str:empresa_id>/', views.data_contingencias, name='contingencias_solicitud'),
    path('process_contingencias/<str:codigoGeneracion>/<str:empresa_id>/', views.procesar_contingencia.as_view(), name='procesar_contingencia'),
    path('dashboard/<str:filtro>/', views.dashboard_data_view, name='dashboard_data_view'),
    path('urls_status/', views.url_status, name='urls_status'),
    path('urls_status/<str:filtro>', views.url_status_data, name='url_status'),
    path('api/login/', views.CustomObtainAuthToken.as_view(), name='api_login'),
    path('api/receptor/<str:codigo>/', views.ReceptorDetail.as_view(), name='receptor-detail'),
    path('api/receptor/', views.ReceptorDetail.as_view(), name='receptor-insert'),
    path('api/proveedor/<str:codigo>/', views.ProveedorDetail.as_view(), name='proveedor-detail'),
    path('api/documentos/', views.DocumentosCreateAPIViews.as_view(), name='documentos-create'),
    path('api/proveedor/', views.ProveedorDetail.as_view(), name='proveedor-insert'),
    path('api/documentos/<str:codigo_generacion>/', views.DocumentosRetrieveAPIViews.as_view(), name='documentos-retrieve'),
    path('api/download-files/<str:codigo_generacion>', views.DownloadFilesAPIs.as_view(), name='download-files'),
    path('api/documentos/<str:codigo_generacion>/update-complete/', views.DocumentosUpdateCompleteAPIView.as_view(), name='documentos-update-complete'),
    path('api/documentoslote/', views.DocumentosLoteCreateAPIViews.as_view(), name='documentos-lote'),  
    path('upadate_lote_data/<str:loteId>/', views.ProcessLoteDocuments.as_view(), name='upadate_lote_data'),  
    path('sentemail/<str:codigoGeneracion>/', views.sent_email, name='sentemail'),
    path('editar-receptor/<str:codigo>/', views.edit_receptor, name='editar_receptor'),
    path('api/invalidar/<str:codigoGeneracion>/', views.invalidarDocumento.as_view(), name='invalidar_documento'),
    path('home/tipo_contingencia', views.tipo_contingecias, name='home_tipos_contigencia'),
    path('contingencia/<str:tipo_contingencia>/<str:motivo>/<str:fecha_inicio>/<str:fecha_fin>/<str:hora_ini>/<str:hora_fin>', views.contingencia.as_view(), name='generate_contingencia'),
    path('api/receptor/<str:telefono>/get_documento/', views.DocumentoClienteTelefonos.as_view(), name='documento-cliente'),
    path('api/receptor/documento/<str:codigo>/', views.DocumentoClientes.as_view(), name='documento-clientes'),
    path('get_receptor/<str:codigoGeneracion>/', views.receptor_from_documents.as_view(), name='cliente_from_document'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)