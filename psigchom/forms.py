from django import forms
from pickle import TRUE
from django.views.generic import View, TemplateView
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from psigcmod.models import Usuario, ContactoBD, Provincia, Municipio, Procedencia
from django.utils.translation import gettext, gettext_lazy as _
from django.conf import settings
from django.contrib import messages

#Create your forms here

class ProcedenForm(forms.ModelForm):
    
    class Meta:
        model = Procedencia
        fields = '__all__'
        #widgets = {"provprocede": s2forms.FixedModelForm}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['municiprocede'].queryset=Municipio.objects.none()
        self.fields['provincia'].widget.attrs.update({'class':'form-control select2', 'style': 'width:45%'})
        self.fields['municipio'].widget.attrs.update({'class':'form-control select2','style': 'width:45%'})
        
        if 'provincia' in self.data:
            try:
                provid = int(self.data.get('prov_id'))
                self.fields['municipio'].queryset = Municipio.objects.filter(provincia=provid).order_by('nombremun')
            except (ValueError, TypeError):
                pass # error_messages = {'invalid': "Contraseña inválida.",'required':"Este campo es obligatorio"}
        #elif self.instance['provprocede'].idprov:
         #   self.fields['municprocede'].queryset=self.instance.provprocede.municiprocede_set.order_by('nombremunicip')
                          
       
class ContactoForm(forms.ModelForm):

    class Meta:
        model = ContactoBD
        fields = ['nombre','ecorreo','asunto','contenido']
        widgets = {"nombre": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Escriba su(s) nombre(s) y apellidos',}),
                "ecorreo": forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Escriba su correo electrónico'}),
                "asunto": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Motivo del contacto'}),
                "contenido": forms.Textarea(attrs={'class':'form-control'})
        }
     
class UsernameField(forms.CharField):
    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
        }

class CrearUserForm(UserCreationForm):

    #provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(),  label='Provincia', widget=forms.Select(attrs={'class': 'form-control select2','autocomplete': 'on',}))
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {'username': UsernameField}
        widgets = {
            'provincia': forms.Select,
        }
      
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden','invalid':'Entrada inválida, por favor, verifique restricciones',
        }
    
    first_name = forms.RegexField(label="Nombre(s)", max_length=50, regex=r'^[\w.@+-]+$',
        help_text = "Escriba su(s) nombre(s) (máximo 50 caracteres de letras, dígitos y @/./+/-/_ unicamente).",
        error_messages = {'required':"Este campo es obligatorio", 'invalid':'Por favor, escriba una cadena de caracteres válida', 'empty':"Por favor, llene este campo"})
    
    last_name = forms.RegexField(label="Apellidos(s)", max_length=50, regex=r'^[\w.@+-]+$', 
        help_text = "Escriba su(s)apellido(s) (máximo 50 caracteres de letras, dígitos y @/./+/-/_ unicamente).",
        error_messages = {'required':"Este campo es obligatorio", 'invalid':'Por favor, escriba una cadena de caracteres válida','blank':"Por favor, llene este campo"})

    username = forms.RegexField(label="Usuario", max_length=30, regex=r'^[\w.@+-]+$',
        help_text = "Escriba un identificador de usuario (máximo 30 caracteres de letras, dígitos y @/./+/-/_ unicamente).",
        error_messages = {'invalid': "Este campo solo puede contener letras, dígitos y @/./+/-/_.",'required':"Este campo es obligatorio",'null':"Por favor, llene este campo "})

    email = forms.RegexField(label="Correo electrónico", max_length=30, regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(attrs={'placeholder': 'Dirección e-mail'}),
        help_text = "Teclee una dirección de correo electrónico válida.",
        error_messages = {'invalid': "Dirección de correro inválida.",'required':"Este campo es obligatorio", })  
    
    password1 = forms.CharField(label="Contraseña",  strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','required':"Este campo es obligatorio"}),
        help_text="Teclee una cadena alfanumérica no menor de 8 caracteres",
        error_messages = {'invalid': "Contraseña inválida",'required':"Este campo es obligatorio"})

    password2 = forms.CharField(label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','required':"Este campo es obligatorio"}),
        strip=False,
        help_text="Teclee la misma contraseña anterior para confirmar.",
        error_messages = {'invalid': "Contraseña inválida.",'required':"Este campo es obligatorio"})
    
    def clean(self):
        super(CrearUserForm, self).clean()
        
        if  self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            self._errors['Contraseñas'] = self.error_class(['Las contraseñas no son válidas o no coinciden' ])

        return self.cleaned_data 

class LoguearUserForm(AuthenticationForm):

    error_messages = {
        'password_mismatch': 'Usuario o contraseña incorrecta',
        }
    username = forms.RegexField(label="Usuario", max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': "Usuario no existe.",'required':"Este campo es obligatorio"})
    
    password = forms.CharField(label="Contraseña",  strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','required':"Este campo es obligatorio"}),
        error_messages = {'invalid': "Contraseña incorrecta",'required':"Este campo es obligatorio"})
    
    def __init__(self, *args, **kwargs):
        super(LoguearUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Identifcador de usuario'})
        self.fields['password'].widget.attrs.update({'class':'form-control', 'placeholder':'Constraseña'})

    class Meta:
        model = Usuario
        fields = ['username', 'password']
        field_classes = {'username': UsernameField}


class PerfilUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre(s)', max_length=50, required=True)
    last_name = forms.CharField(label='Apellido(s)', max_length=50, required=True)
    grupo = forms.CharField( label='Grupo de usuario', max_length=20, disabled = True, required=False )

    class Meta:
        model = Usuario
        fields =['first_name', 'last_name', 'genero', 'municipio', 'grdctfacad', 'princresult', 'grupo']
        