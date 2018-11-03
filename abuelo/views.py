from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from .models import Cuidador
from django.contrib import messages

#sistema de autenticación 
from django.contrib.auth import authenticate,logout, login as auth_login

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'index.html')

def registrar(request):
    run = request.POST.get('run','')
    nombre = request.POST.get('nombre','')
    fechaNacimiento = request.POST.get('fechaNacimiento','')
    correo = request.POST.get('correo','')
    telefono = request.POST.get('telefono','')
    direccion = request.POST.get('direccion','')
    contrasenia = request.POST.get('contrasenia','')

    cuidador = Cuidador.objects.filter(run=run)

    if len(cuidador) == 0 :
        cuidador = Cuidador(run=run, nombre=nombre, fechaNacimiento=fechaNacimiento, correo=correo, telefono=telefono,  direccion=direccion, contrasenia= contrasenia)                
        cuidador.save()
        messages.success(request, 'El usuario fue registrado correctamente.123')
        return render(request,'index.html',{'mensaje':'El usuario fue registrado correctamente.'})
    else:    
        messages.warning(request, 'El usuario ingresado ya esta registrado. 123')
        return render(request,'index.html',{'mensaje':'El usuario ingresado ya esta registrado.'})

def abuelos(request):
    return render(request, 'abuelos.html')

def crear_abuelo(request):
    return render(request, 'crear_abuelo.html')