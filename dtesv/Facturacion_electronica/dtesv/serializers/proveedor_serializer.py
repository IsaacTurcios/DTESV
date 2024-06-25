from rest_framework import serializers
from dtesv.models import Proveedor,C013Municipio 
from .municipio_serializer import MunicipioCodigoField

class ProveedorSerializer(serializers.ModelSerializer):
    municipio = MunicipioCodigoField(queryset=C013Municipio.objects.all())
    class Meta:
        model = Proveedor
        fields = '__all__'
