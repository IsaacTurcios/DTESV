from django import forms
from dtesv.models import Receptor

class ReceptorForm(forms.ModelForm):
    class Meta:
        model = Receptor
        fields = ['tipodocumento',
            'numdocumento',
            'nrc',
            'nombre',
            'codactividad',
            'nombrecomercial',
            'telefono',
            'correo',
            'complemento',
            'municipio',
            'departamento',
            'codpais',
            'tipopersona',
            'tiporeceptor','codigo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar atributo 'id' al campo de correo electrónico
        self.fields['correo'].widget.attrs['id'] = 'id_correo'
        self.fields['codigo'].widget.attrs['readonly'] = True
