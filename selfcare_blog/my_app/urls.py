from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Ruta base
    path('', index, name="index"),

    # Rutas sin consultas a la base de datos
    path('about-us/', about_us, name="about_us"),
    
    # Rutas de usuario
    path('login/', login_request, name="login"),
    path('registro/', register, name="register"),
    path('logout/', logout_request, name="logout"),
    path('perfil/', my_profile, name="profile"),

    # Rutas de publicaciones
    path('category/<str:name>/', category, name="category"),
    path('publicacion/<int:id>/', detail_post, name="detail_post"),
    path('crear-publicacion/', create_post, name="create_post"),
    # Editar publicación
    path('editar-publicacion/<int:id>/', edit_post, name="edit_post"),
    # Eliminar publicación
    path('eliminar-publicacion/<int:id>/', delete_post, name="delete_post"),

    # Ruta de búsqueda
    path('search/', search, name="search"),

    # Ruta de newsletter
    path('newsletter/', newsletter, name="newsletter"),
    
    # Rutas de manejo de errores
    path('error-401/', handler401, name="error_401"),
    path('error-403/', handler403, name="error_403"),
    path('error-404/', handler404, name="error_404"),
    path('error-500/', handler500, name="error_500"),
]
