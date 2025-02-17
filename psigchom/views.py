from email.message import EmailMessage
import logging, json
from django.http import JsonResponse
from pickle import TRUE
from unicodedata import name
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, login, logout, authenticate
from django.contrib import messages
from django import forms
from psycopg2 import IntegrityError
from psigcmod.models import Usuario, ContactoBD, Provincia, Municipio, Procedencia
from django.template import RequestContext
from django.utils.translation import gettext, gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from random import choices
from .forms import ContactoForm, CrearUserForm, LoguearUserForm, PerfilUserForm, ProcedenForm
from django.urls import reverse_lazy


# Create your views here.


def vista_proceden(request):
    provincias = Provincia.objects.all()
    #procedenform=ProcedenForm()
    return render(request, "psigchom/municipioselec.html",{'provincias':provincias})

def vista_getmunics(request):
    provincia_id = request.GET.get('id_provincia')
    print(provincia_id)
    municipios = Municipio.objects.filter(prov=provincia_id).values('idmun', 'nombremun')
    print(municipios)
    return JsonResponse({'municipios': municipios})
    #id_prov=request.Get.get('prov_id')
    #municip=Municipio.objects.filter(provincia_id=id_prov).all()
    #return render(request, "psigchom/getmunicipios.html", {'municipdata':municip})


def vista_inicio(request):
    
    return render(request, "psigchom/index.html")

def vista_codayuda(request):
    return render(request, "psigchom/codayuda.html")


class vista_contacto(CreateView):
    model= ContactoBD
    model = Procedencia
    form_class = ContactoForm
    context_object_name ='contacto'
    template_name = 'contacto.html'
    success_url = reverse_lazy('url_inicio')

    def get(self, request):
        formcontacto=ContactoForm()
        procedenform=ProcedenForm()
        #return render(request, "psigchom/contacto.html", {"contactForm":formcontacto,})
        provincias=Provincia.objects.all()
        municipios=Municipio.objects.all()
        return render(request, "psigchom/contacto.html", {"contactForm":formcontacto, "procedenForm":procedenform, "providata":provincias, "municipdata":municipios})

    def post(self, request):
        formcontacto=ProcedenForm(data=request.POST)
        if formcontacto.is_valid():
            nombrecont=request.POST.get("nombre") + " envió un mensaje de contaco."
            ecorreocont=request.POST.get("ecorreo")
            asuntocont=request.POST.get("asunto")
            contenidocont=request.POST.get("contenido")
            email_from = settings.EMAIL_HOST_USER
            buzon_destino=["carlosap@uclv.edu.cu"]
            enviado=False    
            #emailcontacto=EmailMessage("Mensaje desde el sitio SIGCSSAN","El usuario {} con nombre {} y correo electrónico {} envió este mensaje de contacto:\n\n {}".format(nombrecont,ecorreocont, contenidocont),"",["carlospm08@gmailcom"],reply_to=[ecorreocont])
            if asuntocont!='':
                #send_mail(asuntocont, contenidocont, ecorreocont, buzon_destino,enviado,nombrecont)
                #emailcontacto.send()
                messages.add_message(request=request, level=messages.SUCCESS, message="El mensaje de contacto se ha enviado exitosamente.")
                messages.add_message(request=request, level=messages.WARNING, message="Si en el término de 24 horas aproximadamente no recibe una respuesta en la dirección de correo electrónico escrita por Ud., por favor escriba a esta dirección: carlosap@uclv.edu.cu. Ofrecemos nuestras disculpas por las molestias que la demora pudiera ocasionar.")
                messages.add_message(request=request, level=messages.INFO, message="Para más ayuda sobre el uso del software consulte el MANUAL DE USUARIO.")
                return redirect('url_contacto')
            else:
                messages.add_message(request=request, level=messages.ERROR, message="El mensaje de contacto no pudo ser enviado exitosamente.")
                messages.add_message(request=request, level=messages.ERROR, message="Por favor, verifique estas posibles razones por la que falló el envío (datos del formulario mal escritos, falla en la conexión de salida a la red o servidor).")
                messages.add_message(request=request, level=messages.INFO, message="Para más ayuda sobre el uso del software consulte el MANUAL DE USUARIO.")
                return redirect('url_contacto')
        return render(request, "psigchom/contacto.html", {"contactForm":formcontacto})
    
    def get_context_data(self, **kwargs):
        context = super(vista_contacto).get_context_data(**kwargs)
        context["providata"] = Provincia.objects.all()
        context["municipdata"] = Municipio.objects.all()
        return context
        

class vista_registUser(View):        

    def get(self, request):
        regform=CrearUserForm()
        return render(request, "registro/reg_login_user.html",{"regform":regform})
    
    def post(self, request):
        regform=CrearUserForm(request.POST)
        if regform.is_valid:
            try:
                authuser = Usuario.objects.create_user (username = request.POST['username'], password = request.POST['password1'])
                authuser.first_name = request.POST['first_name']
                authuser.last_name = request.POST['last_name']
                authuser.save()
                login(request,authuser)
                messages.add_message(request=request, level=messages.SUCCESS, message="Usuario creado satisfactoriamente!!!")
                messages.add_message(request=request, level=messages.SUCCESS, message="SEA UD. BIENVENIDO Y GRACIAS POR UTILIZAR ESTE SOFTWARE")
                return redirect('url_inicio')
            except IntegrityError: messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear usuario.")    
        else: messages.add_message(request=request, level=messages.ERROR, message="Error en el formulario, por favor verifique los datos.")
        return render(request, "registro/reg_login_user.html", {"regform":regform})

def vista_loginUser(request): 

    if request.method=="POST":
            loginform=LoguearUserForm(request, data=request.POST)
            if loginform.is_valid:
                authuser=Usuario.objects.filter(username = request.POST['username'])
                if authuser:
                    useractual = authenticate(request, username=request.POST['username'], password=request.POST['password'])
                    if useractual is None:
                        messages.add_message(request=request, level=messages.ERROR, message="Usuario o contraseña incorrectos")
                    else:
                        login(request, useractual)
                        messages.add_message(request=request, level=messages.SUCCESS, message="BIENVENIDO Y GRACIAS POR UTILIZAR 'PESIGC'")
                        return redirect('url_inicio')
                else:
                    messages.add_message(request=request, level=messages.ERROR, message="El usuario con ese identificador no existe en la base de datos")
            else:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar el login")

    loginform=LoguearUserForm(request.POST)
    return render(request, "registro/reg_login_user.html", {"regform":loginform})
        
def sidelogin_form(request):
    authuser=Usuario.objects.filter(username = request.POST['userident'])
    if authuser:
        try:
            authuser = authenticate(request, username=request.POST['userident'], password=request.POST['passident'])
            if authuser is not None:
                login(request, authuser)
                messages.add_message(request=request, level=messages.SUCCESS, message="BIENVENIDO Y GRACIAS POR UTILIZAR 'PSIGC'")
            else:
                messages.add_message(request=request, level=messages.ERROR, message="Usuario o contraseña incorrectos")
        except:
            messages.add_message(request=request, level=messages.ERROR, message="Error al intentar el login")
    else:
        messages.add_message(request=request, level=messages.ERROR, message="El usuario con ese identificador no existe en la base de datos")

    return render(request,"psigchom/index.html")
       
def vista_LogoutUser(request):
    logout(request)
    return redirect('url_inicio')


def vista_PerfilUser(request, id_user):
    upduserperf = Usuario.objects.get(pk = id_user)
    upduserform = PerfilUserForm(instance=upduserperf)
    if request.method == "POST":
        upduserform = PerfilUserForm(request.POST)
        if upduserform.is_valid:
            try: 
                upduserform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Perfil de usuario actualizado exitosamente")    
                return redirect('url_inicio')
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar peril de usuario.")
    return render(request, "registro/perfilUsuario.html", {"perfform":upduserform, "userdata":upduserperf})

