from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombre

class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='img/', null=False)
    titulo = models.CharField(max_length=150, null=False)
    resumen = models.CharField(max_length=350, null=False, blank=True)
    contenido = models.TextField(null=False, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    email = models.EmailField(max_length=254, null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen_perfil = models.ImageField(upload_to='avatars/', null=False, default='avatars/default.jpg')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username

class Newsletter(models.Model):
    email = models.EmailField(max_length=254, null=False, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
