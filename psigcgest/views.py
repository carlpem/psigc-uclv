from django.shortcuts import render, get_object_or_404
from psigcmod.models import Usuario, Noticia, Evento, Documento, Foro, ComentPost, AreaConocimiento
from django.contrib import messages, auth
from django.shortcuts import render, HttpResponse, redirect
from .forms import  PostForm, EventoForm, DocumentoForm, ForoForm, AreaConocForm

# Create your views here.

def vista_gestion(request):
    return render(request, "psigcgest/gestion.html")
#
# SECCIÓN DE NOTICIAS
#
def vista_noticiabd(request):
    noticiasbd = Noticia.objects.all()
    return render(request, "psigcgest/bdnoticias.html", {"noticiasdata":noticiasbd})

def vista_adinoticia(request):
    adinotiform = PostForm()
    try:
        usuactual = get_object_or_404(Usuario, pk=request.user.pk)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar asignar usuario a noticia. Contacte con el administrador del sitio.")    
        redirect('url_noticiabd')
    if request.method =='POST':
        adinotiform = PostForm(data = request.POST)
        if adinotiform.is_valid():
            try:
                prepost = adinotiform.save(commit=False)
                prepost.autor = usuactual
                prepost.tipopub ='Noticia'
                prepost.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="La información ha sido creada exitosamente")
                return redirect('url_noticiabd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear información. Verifique los datos.")    
    return render(request, "psigcgest/edinoticia.html", {'edinotiform':adinotiform})

def vista_edinoticia(request, id_noti):  
    try:
        edinoticia = Noticia.objects.get(idpost=id_noti)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_noticiabd')
    edinotiform = PostForm(instance=edinoticia)
    if request.method=='POST':
        edinotiform = PostForm(request.POST, instance=edinoticia)
        if edinotiform.is_valid():
            try:
                edinotiform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="La información ha sido actualizada exitosamente")
                return redirect('url_noticiabd')
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar la información. Verifique los datos.")
    return render(request, "psigcgest/edinoticia.html", {'edinotiform':edinotiform, 'idpost':id_noti})

def vista_elinoticia(request, id_noti):
    try:
        elinoticia = Noticia.objects.get(idpost=id_noti)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")            
        return redirect('url_noticiabd')
    try:
        elinoticia.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Noticia eliminada satisfactoriamente")
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información.")            
    return redirect('url_noticiabd')
#
#  SECCIÓN EVENTOS
#
def vista_eventobd(request):
    eventosbd = Evento.objects.all()
    return render(request, "psigcgest/bdeventos.html", {"eventosdata":eventosbd})

def vista_adievento(request):
    adieventoform = EventoForm()
    try:
        usuactual = get_object_or_404(Usuario, pk=request.user.pk)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar asignar usuario a evento. Contacte con el administrador del sitio.")    
        redirect('url_eventobd')
    if request.method =='POST':
        adieventoform = EventoForm(data = request.POST)
        if adieventoform.is_valid():
            try:
                prevento = adieventoform.save(commit=False)
                prevento.autor = usuactual
                prevento.tipopub ='Evento'
                prevento.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="La información sobre evento ha sido creada exitosamente")
                return redirect('url_eventobd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear información. Verifique los datos.")    
    return render(request, "psigcgest/edievento.html", {"edieventoform":adieventoform})

def vista_edievento(request, id_event):
    try:
        edievento = Evento.objects.get(idevento=id_event)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_noticiabd')
    edieventoform = EventoForm(instance=edievento)
    if request.method=='POST':
        edieventoform = PostForm(request.POST, instance=edievento)
        if edieventoform.is_valid():
            try:
                edieventoform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="La información ha sido actualizada exitosamente")
                return redirect('url_eventobd')
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar la información. Verifique los datos.")
    return render(request, "psigcgest/edievento.html", {"edieventoform":edieventoform})

def vista_elievento(request, id_event):
    try:
        elievento = Evento.objects.get(idevento=id_event)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")            
        return redirect('url_eventobd')
    try:
        elievento.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de evento eliminado satisfactoriamente")
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información.")            
    return redirect('url_eventobd')
#
#  SECCIÓN DOCUMENTOS
#
def vista_documentobd(request):
    documentosbd = Documento.objects.all()
    return render(request, "psigcgest/bdocumentos.html", {"documentsdata":documentosbd})

def vista_adidocumento(request):
    adidocform = DocumentoForm()
    try:
        usuactual = get_object_or_404(Usuario, pk=request.user.pk)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar asignar usuario a documento. Contacte con el administrador del sitio.")    
        redirect('url_documentobd')
    if request.method =='POST':
        adidocform = DocumentoForm(request.POST, request.FILES)
        if adidocform.is_valid():
            try:
                predoc = adidocform.save(commit=False)
                predoc.autor = usuactual
                predoc.tipopub ='Documento'
                predoc.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="El documento ha sido enviado exitosamente")
                return redirect('url_documentobd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar subir documento. Verifique los datos.")    
    return render(request, "psigcgest/edidocumento.html", {'edidocform':adidocform})

def vista_edidocumento(request, id_doc):  
    try:
        edidocumento = Documento.objects.get(iddoc=id_doc)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_documentobd')
    edidocform = DocumentoForm(instance=edidocumento)
    if request.method=='POST':
        edidocform = DocumentoForm(request.POST, instance=edidocumento)
        if edidocform.is_valid():
            try:
                edidocform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="La información ha sido actualizada exitosamente")
                return redirect('url_documentobd')
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar la información. Verifique los datos.")
    return render(request, "psigcgest/edidocumento.html", {'edidocform':edidocform})

def vista_elidocumento(request, id_doc):
    try:
        elidocumento = Documento.objects.get(iddoc=id_doc)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")            
        return redirect('url_documentobd')
    try:
        elidocumento.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de documento eliminado satisfactoriamente")
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información.")            
    return redirect('url_documentobd')
#
#  SECCIÓN FOROS DE DEBATE
#
def vista_forobd(request):
    foros = Foro.objects.all()
    return render(request, "psigcgest/bdforos.html", {'forosdata':foros})

def vista_adiforo(request):
    adiforoform = ForoForm()
    try:
        usuactual = get_object_or_404(Usuario, pk=request.user.pk)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar asignar usuario a noticia. Contacte con e administrador del sitio.")    
        redirect('url_forobd')
    if request.method =='POST':
        adiforoform = ForoForm(data = request.POST)
        if adiforoform.is_valid():
            try:
                preforo = adiforoform.save(commit=False)
                preforo.moderador = usuactual
                preforo.tipopub ='Foro'
                preforo.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="El foro ha sido creada exitosamente")
                return redirect('url_forobd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear foro. Verifique los datos.")  
    return render(request, "psigcgest/ediforo.html",  {'ediforoform':adiforoform})

def vista_ediforo(request, id_for):
    try:
        ediforo = Foro.objects.get(idforo=id_for)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
        return redirect('url_forobd')
    ediforoform = ForoForm(instance=ediforo)
    if request.method=='POST':
        ediforoform = ForoForm(request.POST, instance=ediforo)
        if ediforoform.is_valid():
            try:
                ediforoform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="La información ha sido actualizada exitosamente")
                return redirect('url_forobd')
            except:
                messages.add_message(request=request, level=messages.ERROR, message="Error al actualizar la información. Verifique los datos.")
    return render(request, "psigcgest/ediforo.html", {'ediforoform':ediforoform})

def vista_eliforo(request, id_for):
    try:
        eliforo = Foro.objects.get(idforo=id_for)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información. Ese registro no existe")            
        return redirect('url_documentobd')
    try:
        eliforo.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Registro de foro eliminado satisfactoriamente")
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar la información.")            
    return redirect('url_forobd')

def vista_edicoment(request, id_coment):
    #try:
    #    edicomentform = ComentForm()
    #    edicoment = ComentPost.objects.get(idcoment=id_coment)
    #    coment = ComentPost.objects.filter()
    #except:
    #    messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar la información. Ese registro no existe")
    #    return redirect('url_forobd')  {'ediforoform':edicomentform}
    return render(request, "psigcgest/ediforo.html")

    
#  SECCIÓN AREAS DEL CONOCIMIENTO
#
def vista_areaconocbd(request):
    areaconoc = AreaConocimiento.objects.all()
    return render(request, "psigcgest/bdareaconoc.html", {'areasdata':areaconoc})

def vista_adiareaconoc(request):
    adareaform = AreaConocForm()
    if request.method =='POST':
        adareaform = AreaConocForm(data = request.POST)
        if adareaform.is_valid():
            try:
                adareaform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="El área del conocimiento fue creada exitosamente")
                return redirect('url_areaconocbd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error al intentar crear área del conocimiento. Verifique los datos.")                
    return render(request, "psigcgest/ediareaconoc.html", {'areaform':adareaform})

def vista_ediareaconoc(request, id_areacon):  
    try:
        updareaconoc = AreaConocimiento.objects.get(idareaconoc=id_areacon)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar editar área del conocimiento. El registor no existe")
        return redirect('url_areaconocbd')    
    updareaform = AreaConocForm(instance=updareaconoc)
    if request.method=='POST':
        updareaform = AreaConocForm(request.POST, instance=updareaconoc)
        if updareaform.is_valid():
            try:
                updareaform.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="El área del conocimiento fue actualizada exitosamente")
                updareaconoc = AreaConocimiento.objects.all()
                return redirect('url_areaconocbd')
            except ValueError:
                messages.add_message(request=request, level=messages.ERROR, message="Error alactualizar área del conocimiento. Verifique los datos.")
    return render(request, "psigcgest/ediareaconoc.html", {'areaform':updareaform})

def vista_elimareaconoc(request, id_areacon):
    try:
        eliareaconoc = AreaConocimiento.objects.get(idareaconoc=id_areacon)
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar área del conocimiento. El registor no existe")
        return redirect('url_areaconocbd')
    try:
        eliareaconoc.delete()
        messages.add_message(request=request, level=messages.SUCCESS, message="Área del conocimiento eliminada satisfactoriamente")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar eliminar área del conocimiento.")            
    return redirect('url_areaconocbd')

def vista_expertosbd(request):
    pass

def vista_demandabd(request):
    pass

def vista_consultabd(request):
    pass
