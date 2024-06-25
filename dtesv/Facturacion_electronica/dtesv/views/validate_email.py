# dtesv/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from dtesv.forms import EmailConfigForm

def validate_email_config(request):
    if request.method == 'POST':
        form = EmailConfigForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Configuración de correo validada correctamente.')
            return redirect('admin:dtesv_emailconfig_changelist')
        else:
            messages.error(request, 'Error en la configuración del correo.')
    else:
        form = EmailConfigForm()

    return render(request, 'admin/validate_email_config.html', {'form': form})
