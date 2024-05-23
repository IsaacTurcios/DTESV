from rest_framework import serializers
from dtesv.models import Receptor ,C013Municipio
from .municipio_serializer import MunicipioCodigoField

class ReceptorSerializer(serializers.ModelSerializer):
    municipio = MunicipioCodigoField(queryset=C013Municipio.objects.all())
    class Meta:
        model = Receptor
        fields = '__all__'
