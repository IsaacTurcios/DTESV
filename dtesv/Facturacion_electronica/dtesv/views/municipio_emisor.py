from django.http import JsonResponse
from dtesv.models import C013Municipio


def get_municipios_by_departamento(request, departamento_id):
    municipios = C013Municipio.objects.filter(cod_departamento_id=departamento_id).values('id', 'nombre')
    return JsonResponse({municipio['id']: municipio['nombre'] for municipio in municipios})
