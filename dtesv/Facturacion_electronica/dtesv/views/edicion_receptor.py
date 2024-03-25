from django.shortcuts import render, get_object_or_404, redirect
from dtesv.models import Receptor
from dtesv.forms import ReceptorForm

def edit_receptor(request, codigo):
    usuario = request.user
    form = None
    mensaje_exito = None

    if usuario.has_perm('dtesv.view_receptor') or usuario.has_perm('dtesv.change_receptor'):
        receptor = get_object_or_404(Receptor, codigo=codigo)
        
        if request.method == 'POST':
            put_data = request.POST.copy()
            if put_data.get('_method') == 'PUT':
                put_data.pop('_method')  # Elimina el campo _method
                put_data.update({'codigo': codigo})  # Añade el código para identificar el receptor

                form = ReceptorForm(put_data, instance=receptor)
                if form.is_valid():
                    fields_list = list(form.changed_data)  # Obtiene los campos modificados
                    if fields_list:  # Si hay cambios
                        receptor.save(update_fields=fields_list)  # Actualiza solo los campos modificados
                        mensaje_exito = 'Cambios guardados.'
            else:
                form = ReceptorForm(instance=receptor)
        else:
            form = ReceptorForm(instance=receptor)
    
    return render(request, 'editar_receptor.html', {'form': form, 'mensaje_exito': mensaje_exito})
