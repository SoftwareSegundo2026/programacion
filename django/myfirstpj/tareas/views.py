from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, RegistroForm, TareaForm
from .models import Profile, Tarea


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Bienvenido! Tu cuenta fue creada.')
            return redirect('getPosts')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})


@login_required
def ver_perfil(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('ver_perfil')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/perfil.html', {'form': form, 'profile': profile})


@login_required
def lista_tareas(request):
    tareas = Tarea.objects.filter(user=request.user).order_by('-fecha', '-created_at')
    return render(request, 'tareas/lista.html', {'tareas': tareas})


@login_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.user = request.user
            tarea.save()
            messages.success(request, 'Tarea creada correctamente.')
            return redirect('lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/formulario.html', {'form': form, 'titulo': 'Crear tarea'})


@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, user=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada correctamente.')
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'tareas/formulario.html', {'form': form, 'titulo': 'Editar tarea'})


@login_required
def eliminar_tarea(request, tarea_id):
    if request.method == 'POST':
        tarea = get_object_or_404(Tarea, id=tarea_id, user=request.user)
        tarea.delete()
        messages.success(request, 'Tarea eliminada.')
    return redirect('lista_tareas')


@login_required
def toggle_tarea(request, tarea_id):
    if request.method == 'POST':
        tarea = get_object_or_404(Tarea, id=tarea_id, user=request.user)
        tarea.completada = not tarea.completada
        tarea.save()
    return redirect('lista_tareas')
