from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from .models import Cuidador
from .models import Remedio
from .models import Abuelo
from .models import Alarma
from django.contrib import messages

#importar user
from django.contrib.auth.models import User
#sistema de autenticación 
from django.contrib.auth import authenticate,logout, login as auth_login

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    usuario = request.session.get('usuario',None)
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

def login_iniciar(request):
    run = request.POST.get('run','')
    contrasenia = request.POST.get('contrasenia','')
    
    #cuidador = authenticate(request,username=run, password=contrasenia)
    #print(cuidador)
    cuidador = Cuidador.objects.filter(run=run).filter(contrasenia=contrasenia)
    print(cuidador)
    if cuidador is not None:
        #auth_login(request, cuidador)
        request.session['usuario'] = cuidador[0].nombre  
        request.session['id'] = cuidador[0].id
        request.session['rut'] = cuidador[0].run
        #request.session['usuario'] = cuidador.first_name+" "+cuidador.last_name

        abuelos = Abuelo.objects.filter(cuidador_id = cuidador[0].id)
        usuario = request.session.get('usuario',None)
        return render(request, 'abuelos.html', {'abuelos':abuelos,'usuario':usuario})
        #return redirect('abuelos')
    else:
        messages.warning(request, 'Las credenciales son incorrectas.')
        return render(request,'index.html',{'mensaje':'Las credenciales son incorrectas.'})

def cerrar_session(request):
    del request.session['usuario']
    return redirect('index')

def abuelos(request):
    usuario = request.session.get('usuario',None)
    return render(request, 'abuelos.html', {'abuelos':Abuelo.objects.all(),'usuario':usuario})


def crear_abuelo(request):
    return render(request, 'crear_abuelo.html', {'titulo':'Crear Abuelo'})

def crear_abuelo_save(request):

    run = request.POST.get('rut','')
    nombre = request.POST.get('nombres','')
    fechaNacimiento = request.POST.get('fecha_nac','')
    
    telefono = request.POST.get('telefono','')
    direccion = request.POST.get('direccion','')
    contrasenia = request.POST.get('contrasenia','')

    foto = request.FILES.get('foto', False)    

    abuelo = Abuelo.objects.filter(run=run)

    if len(abuelo) == 0 : 
        id = request.session.get('id',None)        
        cuidador = Cuidador.objects.get(pk=id)
        abuelo = Abuelo(cuidador=cuidador, run=run, nombre=nombre, fechaNacimiento=fechaNacimiento, telefono=telefono,  direccion=direccion, contrasenia= contrasenia, foto=foto)
        abuelo.save()
        return redirect('abuelos')
    else:    
        return redirect('abuelos')

def editar_abuelo(request,id):
    abuelo = Abuelo.objects.get(pk=id)
    usuario = request.session.get('usuario',None)
    return render(request, 'editar_abuelo.html', {'abuelo':abuelo,'titulo':'Editar Abuelo', 'usuario' : usuario})
    
def perfil(request):
    id = request.session.get('id',None)
    cuidador = Cuidador.objects.get(pk=id)
    usuario = request.session.get('usuario',None)
    
    return render(request, 'perfil.html', {'cuidador': cuidador,'usuario':usuario})

def editar_cuidador(request, id):
    
    run = request.POST.get('run','')
    nombre = request.POST.get('nombre','')
    fechaNacimiento = request.POST.get('fechaNacimiento','')
    correo = request.POST.get('correo','')
    telefono = request.POST.get('telefono','')
    direccion = request.POST.get('direccion','')
    contrasenia = request.POST.get('contrasenia','')

    foto = request.FILES.get('foto', False) 

    cuidador = Cuidador.objects.get(pk=id)
    cuidador.nombre = nombre
    cuidador.fechaNacimiento = fechaNacimiento
    cuidador.correo = correo
    cuidador.telefono = telefono
    cuidador.direccion = direccion
    
    if contrasenia != "" :
        cuidador.contrasenia = contrasenia            

    if foto != False :
        cuidador.foto = foto    

    if cuidador.save() : 
        return redirect('abuelos',{'mensaje':'El usuario fue registrado correctamente.'})
    else:    
        return redirect('abuelos',{'mensaje':'Favor, intente más tarde.'})

def editado_abuelo(request,id):
    abuelo = Abuelo.objects.get(pk=id)

    run = request.POST.get('rut','')
    nombre = request.POST.get('nombres','')
    fechaNacimiento = request.POST.get('fecha_nac','')
    telefono = request.POST.get('telefono','')
    direccion = request.POST.get('direccion','')
    contrasenia = request.POST.get('contrasenia','')
    foto = request.FILES.get('foto', False)

    abuelo.run = run
    abuelo.nombre = nombre
    abuelo.fechaNacimiento = fechaNacimiento
    abuelo.telefono = telefono
    abuelo.direccion = direccion

    if contrasenia != "" :        
        abuelo.contrasenia = contrasenia
    
    if foto != False : 
        abuelo.foto = foto

    abuelo.save()

    return redirect('abuelos')

def eliminar_abuelo(request,id):
    abuelo = Abuelo.objects.get(pk = id)
    abuelo.delete()
    return redirect('abuelos')

def remedio(request, id):
    remedios = Remedio.objects.filter(abuelo_id = id)
    abuelo = Abuelo.objects.get(pk = id)
    usuario = request.session.get('usuario',None)
    return render(request, 'remedio.html', {'remedios': remedios, 'usuario' : usuario, 'abuelo': abuelo})

def crear_remedio(request, id):
    abuelo = Abuelo.objects.get(pk = id)
    usuario = request.session.get('usuario',None)
    return render(request, 'crear_remedio.html', {'abuelo': abuelo,'usuario':usuario})

def creado_remedio(request, id):

    abuelo = Abuelo.objects.get(pk = id)

    nombre = request.POST.get('nombre','')
    descripcion = request.POST.get('descripcion','')
    tratamiento = request.POST.get('tratamiento','')
    horaInicio = request.POST.get('horaInicio','')
    cantVeces = request.POST.get('cantVeces','')

    remedio = Remedio.objects.filter(nombre = nombre)
    usuario = request.session.get('usuario',None)
    remedios = Remedio.objects.filter(abuelo_id = id)
    
    if len(remedio) == 0 : 
        remedio = Remedio(nombre=nombre, descripcion=descripcion, tratamiento=tratamiento, horaInicio=horaInicio, cantVeces=cantVeces,  abuelo=abuelo)
        remedio.save()
        
        crear_alarmas(horaInicio, cantVeces,remedio.id)
        messages.success(request, 'El Remedio fue registrado correctamente.')
        return render(request, 'remedio.html', {'remedios': remedios, 'usuario' : usuario, 'abuelo': abuelo})
    else:    
        messages.warning(request, 'El usuario ingresado ya esta registrado. 123')
        return render(request, 'remedio.html', {'remedios': remedios, 'usuario' : usuario, 'abuelo': abuelo})    

def crear_alarmas(horaInicio, cantVeces, remedio_id):
    rango_horas = 24

    print (cantVeces)
    cantidad = 24 // int(cantVeces)

    for x in range(0, cantidad):      
        if(int(horaInicio) > 23):
            horaInicio = int(horaInicio) - 24
        remedio = Alarma(hora=horaInicio, remedio_id=remedio_id)
        remedio.save()
        
        horaInicio = int(horaInicio) + int(cantVeces)
    return "ok"        

def editar_remedio(request, id):
    remedio = Remedio.objects.get(pk = id)
    usuario = request.session.get('usuario',None)
    return render(request, 'editar_remedio.html', {'remedio': remedio,'usuario':usuario})
    
def editado_remedio(request, id):
    remedio = Remedio.objects.get(pk = id)
    abuelo = remedio.abuelo
    usuario = request.session.get('usuario',None)

    nombre = request.POST.get('nombre','')
    descripcion = request.POST.get('descripcion','')
    tratamiento = request.POST.get('tratamiento','')
    horaInicio = request.POST.get('horaInicio','')
    cantVeces = request.POST.get('cantVeces','')
    
    remedio.nombre = nombre
    remedio.descripcion = descripcion
    remedio.tratamiento = tratamiento
    remedio.horaInicio = horaInicio
    remedio.cantVeces = cantVeces
    
    remedio.save()

    remedios = Remedio.objects.filter(abuelo_id = abuelo.id)
    return render(request, 'remedio.html', {'remedios': remedios, 'usuario' : usuario, 'abuelo': abuelo})

def eliminar_remedio(request, id):
    remedio = Remedio.objects.get(pk = id)
    abuelo = remedio.abuelo

    remedio.delete()

    usuario = request.session.get('usuario',None)
    remedios = Remedio.objects.filter(abuelo_id = abuelo.id)

    return render(request, 'remedio.html', {'usuario':usuario,'abuelo':abuelo,'remedios': remedios})