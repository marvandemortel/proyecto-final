from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Publicacion, Newsletter

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'imagen', 'resumen', 'contenido', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resumen'}),
            'contenido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contenido'}),
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }

class RegistroForm(UserCreationForm):

    # Quitar helptext
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['class'] = 'form-control'
            if fieldname == 'password1':
                self.fields[fieldname].widget.attrs['placeholder'] = 'Contraseña'
            elif fieldname == 'password2':
                self.fields[fieldname].widget.attrs['placeholder'] = 'Confirmar contraseña'

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    imagen_perfil = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'mc-form', 'placeholder': 'Correo electrónico'})
        }
