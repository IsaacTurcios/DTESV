from rest_framework import serializers
from dtesv.models import Receptor, C013Municipio

class MunicipioCodigoField(serializers.RelatedField):
    def to_representation(self, value):
        return value.codigo

    def to_internal_value(self, data):
        try:
            # Obtener el código del municipio del JSON
            codigo = data
            # Obtener el departamento_id de alguna otra manera, por ejemplo, a partir del contexto de la solicitud
            departamento_id = self.context.get('departamento_id')
            # Buscar el municipio en la base de datos que coincida con el código y el departamento_id proporcionados
            municipio = C013Municipio.objects.get(codigo=codigo, cod_departamento_id=departamento_id)
        except C013Municipio.DoesNotExist:
            raise serializers.ValidationError(f"Municipio con código {codigo} y/o departamento {departamento_id} no existe.")
        return municipio

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = C013Municipio
        fields = '__all__'