import os
import time
import django.contrib.auth.models
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import login
from .models import Perfil, Publicacion, Categoria, Newsletter
from .forms import PublicacionForm, RegistroForm, LoginForm
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

def index(request):
    current_path = request.path
    # Obtener todas las categorías
    categorias = Categoria.objects.all()

    # Crear una lista para almacenar la información de las últimas publicaciones por categoría
    ultimas_publicaciones_por_categoria = []

    # Iterar sobre cada categoría
    for categoria in categorias:
        # Obtener la última publicación de la categoría actual
        ultima_publicacion = Publicacion.objects.filter(categoria=categoria).order_by('-fecha_publicacion').first()
        if ultima_publicacion:
            # Obtener el perfil del autor de la última publicación
            perfil_autor = Perfil.objects.get(id=ultima_publicacion.autor_id)
            # Agregar la información de la última publicación y el perfil del autor a la lista
            ultimas_publicaciones_por_categoria.append({
                'categoria': categoria,
                'ultima_publicacion': ultima_publicacion,
                'perfil_autor': perfil_autor
            })

    publicaciones_izq = ultimas_publicaciones_por_categoria.copy()
    publicaciones_der = []

    if len(publicaciones_izq) > 4:
        import random
        # Agregar 4 elementos aleatorios no repetidos a la lista de publicaciones_der
        for i in range(4):
            random_index = random.randint(0, len(publicaciones_izq) - 1)
            publicaciones_der.append(publicaciones_izq.pop(random_index))
    else:
        publicaciones_der = publicaciones_izq.copy()

    return render(request, 'home.html', {'publicaciones_izq': ultimas_publicaciones_por_categoria, 'publicaciones_der': publicaciones_der, 'current_path': current_path})

def about_us(request):
    current_path = request.path
    return render(request, 'about-us.html', {'current_path': current_path})

def category(request, name):
    current_path = request.path
    try:
        if name == "all":
            publicaciones = Publicacion.objects.all()
        else:
            categoria = Categoria.objects.get(nombre=name)
            publicaciones = Publicacion.objects.filter(categoria=categoria)

    except Categoria.DoesNotExist:
        return redirect('error_404')
    
    return render(request, 'category.html', {'publicaciones': publicaciones, 'categoria': name, 'current_path': current_path})

def detail_post(request, id):
    current_path = request.path
    try:
        post = Publicacion.objects.get(id=id)
        autor = Perfil.objects.get(id=post.autor_id)

    except Publicacion.DoesNotExist:
        return redirect('error_404')
    
    return render(request, 'posteo.html', {'post': post, 'autor': autor, 'current_path': current_path})
    

def create_post(request):
    if request.user.is_authenticated:
        current_path = request.path
        if request.method == 'POST':
            form = PublicacionForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    post = form.save(commit=False)
                    post.autor = request.user
                    post.imagen.name = f"{int(time.time())}.png"
                    post.save()
                    return redirect('index')
                except Exception as e:
                    # Manejar cualquier excepción al guardar el post
                    return redirect('error_500')
        else:
            form = PublicacionForm()
        return render(request, 'create-post.html', {'form': form, 'current_path': current_path})
    else:
        return redirect('error_401')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        current_path = request.path
        if request.method == 'POST':
            form = RegistroForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.usuario = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.save()

                # Obtén el archivo de imagen del formulario
                imagen_perfil = form.cleaned_data['imagen_perfil']

                # Verifica si se proporcionó un archivo de imagen
                if imagen_perfil:
                    # Establece el nombre del archivo de imagen
                    imagen_perfil.name = f"avatars/{int(time.time())}.png"
                else:
                    # Si no se proporciona ninguna imagen, crea un archivo de imagen vacío
                    imagen_perfil = SimpleUploadedFile(name=f"{int(time.time())}.png", content=b'')

                # Guarda el objeto de perfil con la imagen de perfil
                perfil = Perfil(email=user.email, imagen_perfil=imagen_perfil, usuario=user)
                perfil.save()
                
                # Inicia sesión al usuario recién registrado
                try:
                    login(request, user)
                    return redirect('index')
                except Exception as e:
                    return redirect('error_500')
            else:
                print(form.errors)
                return render(request, 'register.html', {'form': form, 'current_path': current_path, 'error': True, 'error_type': 'Error al registrar el usuario.'})
        else:
            form = RegistroForm()
        return render(request, 'register.html', {'form': form, 'current_path': current_path})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        current_path = request.path
        if request.method == 'POST':
            form = LoginForm(request, request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect('index')
            else:
                return render(request, 'login.html', {'form': form, 'current_path': current_path, 'error': True, 'error_type': 'Usuario o contraseña incorrectos.'})
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form, 'current_path': current_path})

def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('error_401')

def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('error_401')
    else:
        try:
            new_perfil = Perfil.objects.get(usuario=request.user)
            new_perfil.lastlogin = timezone.localtime(django.contrib.auth.models.User.objects.get(username=request.user).last_login)
            publicaciones = Publicacion.objects.filter(autor=request.user)
        except Perfil.DoesNotExist:
            return redirect('error_404')

    current_path = request.path

    return render(request, 'profile.html', {'perfil': new_perfil, 'publicaciones': publicaciones, 'current_path': current_path})

def newsletter(request):
    current_path = request.path

    if request.method == 'POST':
        try:
            email = request.POST['email']
            newsletter = Newsletter(email=email)
            newsletter.save()
            return redirect('index')
        except Exception as e:
            return redirect('error_500')
        
    return render(request, 'newsletter.html', {'current_path': current_path})

def handler401(request, exception = None):
    if request.user.is_authenticated:
        return handler403(request)
    else:
        return redirect('login')
    
def handler403(request, exception = None):
    return render(request, '403.html', status=403, context={'exception': exception})

def handler404(request, exception = None):
    return render(request, '404.html', status=404, context={'exception': exception})

def handler500(request, exception = None):
    return render(request, '500.html', status=500, context={'exception': exception})

def edit_post(request, id):
    if request.user.is_authenticated:
        current_path = request.path
        try:
            post = Publicacion.objects.get(id=id)
            if request.user == post.autor:
                if request.method == 'POST':
                    form = PublicacionForm(request.POST, request.FILES, instance=post)
                    if form.is_valid():
                        form.save()
                        return redirect('index')
                else:
                    form = PublicacionForm(instance=post)
                return render(request, 'update-post.html', {'form': form, 'current_path': current_path})
            else:
                return redirect('error_403')
        except Publicacion.DoesNotExist:
            return redirect('error_404')
    else:
        return redirect('error_401')
    
def delete_post(request, id):
    if request.user.is_authenticated:
        try:
            post = Publicacion.objects.get(id=id)
            if request.user == post.autor:
                post.delete()                
                if os.path.exists(post.imagen.path):
                    print("The file exists")
                    os.remove(post.imagen.path)
                    print("The file has been deleted")
                else:
                    print("The file does not exist")                
                return redirect('index')
            else:
                return redirect('error_403')
        except Publicacion.DoesNotExist:
            return redirect('error_404')
    else:
        return redirect('error_401')
    
def search(request):
    current_path = request.path
    query = request.GET.get('q')
    if query:
        publicaciones = Publicacion.objects.filter(titulo__icontains=query)
    else:
        publicaciones = None
    return render(request, 'resultados-busqueda.html', {'query': query, 'publicaciones': publicaciones, 'current_path': current_path})