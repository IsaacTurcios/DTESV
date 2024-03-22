from django.contrib.auth.models import AbstractUser ,Group,Permission
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password




class User(AbstractUser):
    puede_procesar_contingencia = models.BooleanField(default=False)
    #puede_re_procesar = models.BooleanField(default=False)
   # companies = models.ManyToManyField('dtesv.Company', related_name='users_company')
    #companies = models.ForeignKey('dtesv.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='users_company')

    def save(self, *args, **kwargs):
        if self.password:
            # Verifica si la contraseña está cambiando
            if not self.pk:
                # Si el usuario es nuevo, encripta la contraseña
                self.password = make_password(self.password)
            else:
                # Si el usuario ya existe, compara la contraseña actual con la nueva
                usuario_actual = User.objects.get(pk=self.pk)
                if self.password != usuario_actual.password:
                   # self.password = make_password(self.password)
                    print('Contraseña Cambiada')
        super().save(*args, **kwargs)
    def __str__(self):
        return self.email
    

    
  