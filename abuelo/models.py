from django.db import models

# Create your models here.

class Cuidador(models.Model):
    run = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    direccion = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=10)
    contrasenia = models.CharField(max_length=30)
    
    def __str__(self):
        return "CUIDADOR"

class Abuelo(models.Model):
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos/')
    run = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    telefono = models.CharField(max_length=10)
    contrasenia = models.CharField(max_length=30)
    
    def __str__(self):
        return "ABUELO"

class Remedio(models.Model):
    abuelo = models.ForeignKey(Abuelo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    tratamiento = models.CharField(max_length=100)
    horaInicio = models.IntegerField()     
    cantVeces = models.IntegerField()

    def __str__(self):
        return "REMEDIO"

class Alarma(models.Model):
    remedio = models.ForeignKey(Remedio, on_delete=models.CASCADE)
    hora = models.IntegerField()  

    def __str__(self):
        return "ALARMA"

class Historial(models.Model):
    abuelo = models.ForeignKey(Abuelo, on_delete=models.CASCADE)
    alarma = models.ForeignKey(Alarma, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=2)
