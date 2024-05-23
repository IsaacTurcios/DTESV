from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from .models import User , Company ,Parametros ,Emisor ,Vendedores,Sucursales,C013Municipio
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
# Register your models here.
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

    def clean_password(self):
        password = self.cleaned_data.get("password")
        user = self.instance

        try:
            validate_password(password,user.username)
        except ValidationError as e:
            raise ValidationError({'password': ', '.join(e.messages)})

        return password

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

class CompanyAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

class SucursalesAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)


class EmisorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "municipio":
            # Inicialmente, mostrar un queryset vacío
            kwargs["queryset"] = C013Municipio.objects.none()
            
            # Obtener el valor del departamento del POST o del objeto instanciado
            if request.method == 'POST':
                departamento_id = request.POST.get('departamento')
            else:  # Para GET requests, obtén el departamento del objeto que se está editando
                obj_id = request.resolver_match.kwargs.get('object_id')
                if obj_id:
                    try:
                        obj = self.model.objects.get(pk=obj_id)
                        departamento_id = obj.departamento_id
                        kwargs["queryset"] = C013Municipio.objects.filter(cod_departamento=departamento_id)
                    except self.model.DoesNotExist:
                        departamento_id = None
                else:
                    departamento_id = None

            # Si tenemos un departamento_id, filtrar los municipios
            if departamento_id:
                kwargs["queryset"] = C013Municipio.objects.filter(cod_departamento=departamento_id)
            
            formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
            formfield.widget = RelatedFieldWidgetWrapper(
                formfield.widget, db_field.remote_field, self.admin_site
            )
            return formfield
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('js/emisor_admin.js',)

admin.site.register(User,CustomUserAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Parametros)
admin.site.register(Emisor,EmisorAdmin)
admin.site.register(Vendedores)
admin.site.register(Sucursales,SucursalesAdmin)


admin.site.site_header = 'Panel de Administración DTESV'
