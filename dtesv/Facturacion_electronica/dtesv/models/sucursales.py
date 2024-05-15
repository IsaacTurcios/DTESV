from django.db import models
from django.conf import settings
from .user import User
import os
from django.utils.deconstruct import deconstructible

from django.core.files.storage import FileSystemStorage
 

#current_directory = os.path.dirname(os.path.abspath(__file__))
#directorio_actual = os.getcwd()
#mymodule_dir = os.path.join( directorio_actual, 'Facturacion_electronica\\dtesv' )
#logos_dir = os.path.join( mymodule_dir, 'company_logos' )

#fs = FileSystemStorage(location='/opt/DTESV/dtesv/Facturacion_electronica/dtesv/company_logos/')


class Sucursales(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='sucursal_users', blank=True)
    company_id = models.ForeignKey('Company', models.DO_NOTHING, db_column='company_id',default= 1, blank=False, null=False,related_name = 'sucursal_company' )  # Field name made lowercase. 
    factura = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    cCredito = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    notaRemision = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    notaCredito = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    notaDebito = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    cRetencion = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    cLiquidacion = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    docLiquidacion = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    facExportacion = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    sujetoExcluido = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    cDonacion = models.CharField(max_length=15, blank=False, null=False, default='000000000000001')
    susursalMH = models.CharField(max_length=4, blank=False, null=False, default='0001')
    cajaMH = models.CharField(max_length=4, blank=False, null=False, default='0001')

    def __str__(self):
        return self.name