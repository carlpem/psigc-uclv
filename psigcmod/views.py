from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect
from .models import Provincia, Municipio, Oace
from .models import Usuario, InfoEjes, ProgDesarrollo, EntidActor
from .forms import OaceForm, EntidActorForm, ProgDesaForm, EjeInfoForm, UsuarioForm
from psigchom.forms import PerfilUserForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def load_municipio(request):
    prov_id = request.GET.get('idprovinc')
    selecmuni = Municipio.objects.filter(idprov=prov_id)
    return render(request, "psigcmod/ediejeformacbd.html", {'munidata':selecmuni})

def vista_basesdatos(request):
    return render(request, "psigcmod/basesdatos.html")
#
# SECCIÓN INFORMACIÓN EJES
#     
def vista_ejesbd(request):
    ejes = InfoEjes.objects.all()
    return render(request, "psigcmod/tableregistros.html", {'ejesdata':ejes})

def vista_adieje(request):
    adiejeinfoform = EjeInfoForm()
    error=None
    if request.method =='POST':
        adiejeinfoform = EjeInfoForm(request.POST)
        if adiejeinfoform.is_valid():
            try:
                adiejeinfoform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Los datos del registro han sido guardados exitosamente")
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Verifique datos o conexión.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")
            error=adiejeinfoform.errors 

    return render(request, "psigcmod/ediejeinfo.html", {'dataform':adiejeinfoform, 'errores':error})

def vista_ediejeinfo(request, id_eje):
    try:
        updeje = InfoEjes.objects.get(idinfo=id_eje)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_ejesbd')
    ediejeinfoform = EjeInfoForm(instance=updeje)
    error=None
    if request.method=='POST':
        ediejeinfoform = EjeInfoForm(request.POST, instance=updeje)
        if ediejeinfoform.is_valid():
            try:
                ediejeinfoform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Los datos del registro han sido guardado exitosamente")
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar la información. Verifique los mensajes.")
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=ediejeinfoform.errors 
    return render(request, "psigcmod/ediejeinfo.html", {"dataform":ediejeinfoform, 'errores':error})

def vista_elieje(request, id_eje):
    try:
        elieje = InfoEjes.objects.get(idinfo=id_eje)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")
        return redirect('url_ejesbd')
    try:
        elieje.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de datos eliminado exitosamente")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar registro.")            
    return redirect('url_ejesbd')
#
# SECCIÓN USUARIOS
#
def vista_usuariobd(request):
    usuariobd = Usuario.objects.all()
    return render(request, "psigcmod/bdusuarios.html", {'usuariosdata':usuariobd})

def vista_adiusuariobd(request):
    adiusuarioform = UsuarioForm()
    error=None
    if request.method =='POST':
        adiusuarioform = UsuarioForm(data = request.POST)
        if adiusuarioform.is_valid():
            try:
                adiusuarioform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro de usuario creado exitosamente")
                return redirect('url_usuariobd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=adiusuarioform.errors         
    return render(request, "psigcmod/ediusuario.html", {'usuarioform':adiusuarioform})

def vista_ediusuariobd(request, id_usua):
    try:
        updusua = Usuario.objects.get(id=id_usua)  
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_usuariobd')    
    updusuaform = UsuarioForm(instance=updusua)
    error=None
    if request.method=='POST':
        updusuaform = UsuarioForm(request.POST, instance=updusua)
        if updusuaform.is_valid():
            #if not request.POST['princresult']=="":
            #    updusua.princresult=request.POST['princresult']
            #else: 
            updusua.princresult='Principales temas y resultados de investigación aún sin especificar' 
            try:
                updusuaform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Perfil de usuario actualizado exitosamente")
                updusua = Usuario.objects.all()
                return redirect('url_usuariobd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar perfil de usuario, verifique los datos.")
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=updusuaform.errors 
    return render(request, "psigcmod/ediusuario.html", {'usuarioform':updusuaform})

def vista_eliusuariobd(request, id_usua):
    try:
        eliusua = Usuario.objects.get(id=id_usua)  
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar borrar la información. Ese registro no existe")
        return redirect('url_usuariobd')
    try:
        eliusua.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de usuario eliminado satisfactoriamente")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar registro de usuario.")            
    return redirect('url_usuariobd')
#
# SECCIÓN OACES
#
def vista_oacebd(request):
    oace = Oace.objects.all()
    return render(request, "psigcmod/bdoaces.html", {'oacedata':oace})

def vista_adioace(request):
    adioaceform = OaceForm()
    error = None
    if request.method =='POST':
        adioaceform =OaceForm(data = request.POST)
        if adioaceform.is_valid():
            try:
                adioaceform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Organismo del Estado creado exitosamente")
                return redirect('url_oacebd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=adioaceform.errors 
    return render(request, "psigcmod/edioace.html", {'oaceform':adioaceform})

def vista_edioace(request, id_oace):
    try:
        updataoace = Oace.objects.get(idoace=id_oace)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_oacebd')
    edioaceform = OaceForm(instance=updataoace)
    error = None
    if request.method =='POST':
        edioaceform =OaceForm(request.POST, instance=updataoace)
        if edioaceform.is_valid():
            try:
                edioaceform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Organismo del Estado actualizado exitosamente")
                updataoace = Oace.objects.all()
                return redirect('url_oacebd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar actualizar registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error = edioaceform.errors 
    return render(request, "psigcmod/edioace.html", {'oaceform':edioaceform})

def vista_elioace(request, id_oace):
    try:
        elioace = Oace.objects.get(idoace=id_oace)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")
        return redirect('url_oacebd')
    try:
        elioace.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Organismo del Estado eliminado satisfactoriamente")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar registro.")            
    return redirect('url_oacebd')

# SECCIÓN PROGRAMAS DE DESARROLLO

def vista_progdesabd(request):
    prgdesarr = ProgDesarrollo.objects.all()
    return render(request, "psigcmod/bdprgdesarr.html", {'prgdesadata':prgdesarr})

def vista_adiprogdesa(request):
    adiprgdesaform = ProgDesaForm()
    error=None
    if request.method =='POST':
        adiprgdesaform =ProgDesaForm(data = request.POST)
        if adiprgdesaform.is_valid():
            try:
                adiprgdesaform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro para Programa de desarrollo creado exitosamente")
                return redirect('url_progdesabd')
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=adiprgdesaform.errors         
    return render(request, "psigcmod/ediprogdesa.html", {'prgdesaform':adiprgdesaform})

def vista_ediprogdesa(request, id_prog):
    try:
        updprgdesa = ProgDesarrollo.objects.get(idprog=id_prog)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_progdesabd')
    ediprgdesaform = ProgDesaForm(instance=updprgdesa)
    error = None
    if request.method =='POST':
        ediprgdesaform =ProgDesaForm(request.POST, instance=updprgdesa)
        if ediprgdesaform.is_valid():
            try:
                ediprgdesaform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Programa de desarrollo actualizado exitosamente")
                return redirect('url_progdesabd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar actualizar registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=ediprgdesaform.errors 
    return render(request, "psigcmod/ediprogdesa.html", {'prgdesaform':ediprgdesaform})

def vista_eliprogdesa(request, id_prog):
    try:
        eliprgdesa = ProgDesarrollo.objects.get(idprog=id_prog)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")
        return redirect('url_progdesabd')
    try:
        eliprgdesa.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Programa de desarrollo eliminado satisfactoriamente")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar registro.")            
    return redirect('url_progdesabd')
#
# SECCIÓN ENTIDADES ACTORES
#
def vista_entidactbd(request):
    entidad = EntidActor.objects.all()
    return render(request, "psigcmod/bdentidact.html", {'entidata':entidad})

def vista_adientidact(request):
    adientidactform = EntidActorForm()
    if request.method =='POST':
        adientidactform =EntidActorForm(data = request.POST)
        error = None
        if adientidactform.is_valid():
            try:
                adientidactform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro para Entidad-Actor creado exitosamente")
                return redirect('url_entidactbd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=adientidactform.errors 
    return render(request, "psigcmod/edientidact.html", {'entidactform':adientidactform})

def vista_edientidact(request, id_actor):
    try:
        updentidactor = EntidActor.objects.get(idactor=id_actor)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_ejesbd')
    edientidactform = EntidActorForm(instance=updentidactor)   
    if request.method =='POST':
        edientidactform = EntidActorForm(request.POST, instance=updentidactor)
        error = None
        if edientidactform.is_valid():
            try:
                edientidactform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Registro para Entidad-Actor actualizado exitosamente")
                return redirect('url_entidactbd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar actualizar registro. Por favor, verifique los datos.")    
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
            error=edientidactform.errors 
    return render(request, "psigcmod/edientidact.html", {'entidactform':edientidactform})

def vista_elientidact(request, id_actor):
    try:
        elientidactor = EntidActor.objects.get(idactor=id_actor)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")
        return redirect('url_entidactbd')
    try:
        elientidactor.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Entidad-Actor eliminado satisfactoriamente")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar registro.")            
    return redirect('url_entidactbd') 
#
# SECCIÓN PROYECTOS DE INVESTIGACION
#
#def vista_proyinvestbd(request):
#    proyinvest = ProyInvest.objects.all()
#    return render(request, "psigcmod/bdproyinvest.html", {'proyinvestdata':proyinvest})

#def vista_adiproyinvest(request):
#    adiproyinvestform = ProyInvestForm()
#    if request.method =='POST':
#        adiproyinvestform =ProyInvestForm(data = request.POST)
#        error =None
#        if adiproyinvestform.is_valid():
#            try:
#                adiproyinvestform.save()
#                messages.add_message(request=request, level=messages.SUCCESS, message="Registro para proyecto de investigación creado exitosamente")
#                return redirect('url_proyinvestbd')
#            except ValueError:
#                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Por favor, verifique los datos.")
#        else:
#            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
#            error=adiproyinvestform.errors 
#    return render(request, "psigcmod/ediproyinvest.html", {'proyinvestform':adiproyinvestform})

#def vista_ediproyinvest(request, id_proy):
#    try:
#        updproyinvest = ProyInvest.objects.get(idproy=id_proy)
#    except:
#        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
#        return redirect('url_proyinvestbd')
#    ediproyinvestform = ProyInvestForm(instance=updproyinvest)   
#    if request.method =='POST':
#        ediproyinvestform =ProyInvestForm(request.POST, instance=updproyinvest)
#        error =None
#        if ediproyinvestform.is_valid():
#            try:
#                ediproyinvestform.save()
#                messages.add_message(request=request, level=messages.SUCCESS, message="Registro para proyecto de investigación creado exitosamente")
#                return redirect('url_proyinvestbd')
#            except ValueError:
#                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear registro. Por favor, verifique los datos.")
#        else:
#            messages.add_message(request=request, level=messages.ERROR, message="Existen errores en los datos. Verifique los mensajes")        
#            error=ediproyinvestform.errors 
#    return render(request, "psigcmod/ediproyinvest.html", {'proyinvestform':ediproyinvestform})

#def vista_eliproyinvest(request, id_proy):
#    try:
#        eliproyinvest = ProyInvest.objects.get(idproy=id_proy)
#    except:
#        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")
#        return redirect('url_proyinvestbd')
#    try:
#        eliproyinvest.delete()
#        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de Proyecto de investigación eliminado satisfactoriamente")
#    except ValueError:
#        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar registro.")            
#    return redirect('url_proyinvestbd') 
#



