from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from .models import Cuidador
from .models import Remedio
from .models import Abuelo
from .models import Alarma
from .models import Historial
from django.contrib import messages
from django.http import JsonResponse

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
    print("ajax request")
    run = request.POST.get('run','')
    nombre = request.POST.get('nombre','')
    fechaNacimiento = request.POST.get('fechaNacimiento','')
    correo = request.POST.get('correo','')
    print("ajax request correo")
    telefono = request.POST.get('telefono','')
    direccion = request.POST.get('direccion','')
    contrasenia = request.POST.get('contrasenia','')

    cuidador = Cuidador.objects.filter(run=run)

    if len(cuidador) == 0 :
        cuidador = Cuidador(run=run, nombre=nombre, fechaNacimiento=fechaNacimiento, correo=correo, telefono=telefono,  direccion=direccion, contrasenia= contrasenia)                
        cuidador.save()

        data = {
        'mensaje': 'El usuario fue registrado correctamente.',
        'type' : 'success',
        'tittle': 'Registro exitoso!'
        }
        
        return JsonResponse(data)
        #return render(request,'index.html',{'mensaje':'El usuario fue registrado correctamente.'})
    else:
        data = {
        'mensaje': 'El usuario ingresado ya esta registrado.',
        'type' : 'error',
        'tittle': 'Error!'
        }
        return JsonResponse(data)
        #return render(request,'index.html',{'mensaje':'El usuario ingresado ya esta registrado.'})

def login_iniciar(request):
    run = request.POST.get('run','')
    contrasenia = request.POST.get('contrasenia','')
    
    #cuidador = authenticate(request,username=run, password=contrasenia)
    #print(cuidador)
    cuidador = Cuidador.objects.filter(run=run).filter(contrasenia=contrasenia)
    print(cuidador)
    if len(cuidador) > 0:
        #auth_login(request, cuidador)
        request.session['usuario'] = cuidador[0].nombre  
        request.session['id'] = cuidador[0].id
        request.session['rut'] = cuidador[0].run
        #request.session['usuario'] = cuidador.first_name+" "+cuidador.last_name

        abuelos = Abuelo.objects.filter(cuidador_id = cuidador[0].id)
        usuario = request.session.get('usuario',None)
        data = { 
            'mensaje': 'Bienvenido!!!', 
            'type' : 'success', 
            'tittle': 'Inicio Sesión!', 
            'tipo' : 'cuidador' 
        } 
         
        return JsonResponse(data) 
        #return render(request, 'abuelos.html', {'abuelos':abuelos,'usuario':usuario})
        
    else:
        abuelo = Abuelo.objects.filter(run=run).filter(contrasenia=contrasenia)

        if len(abuelo) > 0:
            request.session['usuario'] = abuelo[0].nombre  
            request.session['id'] = abuelo[0].id
            request.session['rut'] = abuelo[0].run

            usuario = request.session.get('usuario',None)
            
            data = { 
                'mensaje': 'Bienvenido!!!', 
                'type' : 'success', 
                'tittle': 'Inicio Sesión!', 
                'tipo' : 'abuelo' 
            } 
             
            return JsonResponse(data) 
            #return redirect('abuelo_remedios')
        else :
            data = { 
            'mensaje': 'Las credenciales son incorrectas.', 
            'type' : 'error', 
            'tittle': 'Inicio Sesión!' 
            } 
            return JsonResponse(data) 
            #return render(request,'index.html',{'mensaje':'Las credenciales son incorrectas.'})

def cerrar_session(request):
    del request.session['usuario']
    return redirect('index')

def abuelos(request):
    usuario = request.session.get('usuario',None)
    id = request.session.get('id',None)

    return render(request, 'abuelos.html', {'abuelos':Abuelo.objects.all().filter(cuidador_id = id),'usuario':usuario})


def crear_abuelo(request):
    usuario = request.session.get('usuario',None) 
    return render(request, 'crear_abuelo.html', {'usuario':usuario})

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
        data = { 
            'mensaje': 'El abuelo fue registrado correctamente.', 
            'type' : 'success', 
            'tittle': 'Registro abuelo' 
        } 
        return JsonResponse(data) 
        #return redirect('abuelos')
    else:    
        data = { 
            'mensaje': 'Error al registrar abuelo. El rut ya existe.', 
            'type' : 'error', 
            'tittle': 'Registro abuelo' 
        } 
        return JsonResponse(data)
        #return redirect('abuelos')

def editar_abuelo(request,id):
    abuelo = Abuelo.objects.get(pk=id)
    usuario = request.session.get('usuario',None)
    return render(request, 'editar_abuelo.html', {'abuelo':abuelo, 'usuario' : usuario})
    
def perfil(request):
    id = request.session.get('id',None)
    cuidador = Cuidador.objects.get(pk=id)
    usuario = request.session.get('usuario',None)
    
    return render(request, 'perfil.html', {'cuidador': cuidador,'usuario':usuario})

def editar_cuidador(request, id):
    
    try:
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

        cuidador.save() 
        request.session['usuario'] = cuidador.nombre
        data = { 
            'mensaje': 'Los datos fueron editados correctamente.', 
            'type' : 'success', 
            'tittle': 'Editar perfil' 
        } 
        return JsonResponse(data)
    except:
        data = { 
            'mensaje': 'Error al editar los datos.', 
            'type' : 'success', 
            'tittle': 'Editar perfil' 
        } 
        return JsonResponse(data)


def editado_abuelo(request,id):

    try:
        abuelo = Abuelo.objects.get(pk=id)

        run = request.POST.get('rut','')
        nombre = request.POST.get('nombres','')
        fechaNacimiento = request.POST.get('fecha_nac','')
        telefono = request.POST.get('telefono','')
        direccion = request.POST.get('direccion','')
        contrasenia = request.POST.get('contrasenia','')
        foto = request.FILES.get('foto', False)
        
        abuelo.nombre = nombre
        abuelo.fechaNacimiento = fechaNacimiento
        abuelo.telefono = telefono
        abuelo.direccion = direccion

        if contrasenia != "" :        
            abuelo.contrasenia = contrasenia
        
        if foto != False : 
            abuelo.foto = foto

    
        abuelo.save()
        data = { 
            'mensaje': 'El abuelo fue editar correctamente.', 
            'type' : 'success', 
            'tittle': 'Editar abuelo' 
        } 
        return JsonResponse(data)
    except:
        data = { 
            'mensaje': 'Error al editar abuelo.', 
            'type' : 'success', 
            'tittle': 'Editar abuelo' 
        } 
        return JsonResponse(data)


def eliminar_abuelo(request,id):
    try:

        abuelo = Abuelo.objects.get(pk = id)
        abuelo.delete()

        data = { 
            'mensaje': 'El abuelo fue eliminado correctamente.', 
            'type' : 'success', 
            'tittle': 'Eliminar abuelo' 
        } 
        return JsonResponse(data)
    except:
        data = { 
            'mensaje': 'Error al eliminar abuelo.', 
            'type' : 'error', 
            'tittle': 'Eliminar abuelo' 
        } 
        return JsonResponse(data)

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

    remedio = Remedio.objects.filter(abuelo_id = abuelo.id).filter(nombre = nombre)
    usuario = request.session.get('usuario',None)
    
    if len(remedio) == 0 : 
        remedio = Remedio(nombre=nombre, descripcion=descripcion, tratamiento=tratamiento, horaInicio=horaInicio, cantVeces=cantVeces,  abuelo=abuelo)
        remedio.save()
        
        crear_alarmas(horaInicio, cantVeces,remedio.id)
        data = { 
            'mensaje': 'El remedio fue registrado correctamente.', 
            'type' : 'success', 
            'tittle': 'Registro remedio' 
        } 
        return JsonResponse(data) 
    else:    
        data = { 
            'mensaje': 'El remedio ya esta registrado.', 
            'type' : 'error', 
            'tittle': 'Registro remedio' 
        } 
        return JsonResponse(data)

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
    abuelo = Abuelo.objects.get(pk = remedio.abuelo_id)
    usuario = request.session.get('usuario',None)
    return render(request, 'editar_remedio.html', {'remedio': remedio,'usuario':usuario, 'abuelo':abuelo})
    
def editado_remedio(request, id):
    try:
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

        Alarma.objects.filter(remedio_id = remedio.id).delete()
        crear_alarmas(horaInicio, cantVeces,remedio.id)
        
        data = { 
            'mensaje': 'El remedio fue editado correctamente.', 
            'type' : 'success', 
            'tittle': 'Editar remedio' 
        } 
        return JsonResponse(data)
        
        
    except:
        data = { 
            'mensaje': 'Error al editar el remedio.', 
            'type' : 'success', 
            'tittle': 'Editar remedio' 
        } 
        return JsonResponse(data)
        
def eliminar_remedio(request, id):
    remedio = Remedio.objects.get(pk = id)
    abuelo = remedio.abuelo

    remedio.delete()

    Alarma.objects.filter(remedio_id = remedio.id).delete()

    usuario = request.session.get('usuario',None)
    remedios = Remedio.objects.filter(abuelo_id = abuelo.id)

    return render(request, 'remedio.html', {'usuario':usuario,'abuelo':abuelo,'remedios': remedios})

def abuelo_remedios(request):
    usuario = request.session.get('usuario', None)
    id = request.session.get('id', None)
    
    abuelo = Abuelo.objects.get(pk = id)    
    remedios = Remedio.objects.filter(abuelo_id = abuelo.id)
    alarmas = []

    for x in range(0, len(remedios)):
        alarmas.append(Alarma.objects.filter(remedio_id = remedios[x].id))

    return render(request, 'abuelo_remedios.html', {'alarmas': alarmas, 'usuario': usuario, 'abuelo': abuelo})

def ver_alarmas(request, id):
    alarmas = Alarma.objects.filter(remedio_id = id)
    remedio = Remedio.objects.get(pk = id)
    abuelo = Abuelo.objects.get(id = remedio.abuelo_id)

    usuario = request.session.get('usuario',None)
    return render(request, 'ver_alarmas.html', {'alarmas': alarmas, 'usuario': usuario, 'abuelo': abuelo})

#def registrar_consumo_remedio(request, abuelo_id, alarma_id):
#    abuelo_id = request.POST.get('abuelo_id','')
#    alarma_id = request.POST.get('alarma_id','')
#    estado = request.POST.get('estado','')
        
    #fecha_ahora = datetime.strptime(datetime.now(), "%d-%b-%Y %H:%M:%S")
    #historial = Historial(estado = estado, fecha = fecha_ahora, abuelo_id = abuelo_id, alarma_id=alarma_id)
    #historial.save()
    
#    return redirect('abuelos_remedios')