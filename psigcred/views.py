
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from email.message import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from psigcmod.models import AreaConocimiento, Usuario, Noticia, Evento, Documento, Foro, ComentPost, ComentReply, Publicacion
#from psigcmod.forms import AreaConocForm
from .forms import DemandaForm, ComentForm, ReplyComentForm
from django.contrib import messages


# Create your views here.

def vista_redconoc(request):
    try:
        publicdata = Publicacion.objects.all()
        areacondata = AreaConocimiento.objects.all()
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar las publicaciones.")
        return redirect('url_redconoc')
    try:
        areacondata = AreaConocimiento.objects.all()
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar las areas del conocimento.")
        return redirect('url_redconoc')
    usuarios = Usuario.objects.all()

    return render(request, "psigcred/titulares.html", {'publicaciones':publicdata, 'areasdata': areacondata, 'perfiles':usuarios})

def vista_areasconoc(request):
    areacondata = AreaConocimiento.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, "psigcred/tableareasconoc.html", {'areasdata':areacondata, 'perfiles':usuarios})

def vista_expertos(request):
    expertos = Usuario.objects.all()
    return render(request, "psigcred/tableexpertos.html", {"expertossdata":expertos})
    
def vista_noticia(request):
    try:
        noticias = Noticia.objects.all() 
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar las noticias.")
        return redirect('url_redconoc')
    
    return render(request, "psigcred/tablenoticias.html", {"noticiasdata":noticias})

def vista_leernoticia(request, id_post):
    try:
        noticia = Noticia.objects.get(idpost=id_post)
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar detalles de la noticia. Ese registro no existe")
        return redirect('url_noticia')  
    
    return render(request, "psigcred/noticialeer.html", {"leernoticia":noticia})

def vista_evento(request):
    try:
        eventos = Evento.objects.all()
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los eventos registrados.")
        return redirect('url_redconoc')  
    return render(request, "psigcred/tableeventos.html", {"eventosdata":eventos})

def vista_documento(request):
    try:
        documentos = Documento.objects.all()
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los documentos subidos a la PESIGC.")
        return redirect('url_redconoc')  
    return render(request, "psigcred/tabledocument.html", {"documendata":documentos})

def vista_foro(request):
    try:
            foros = Foro.objects.all()
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los foros.")
        return redirect('url_redconoc')  
    return render(request, "psigcred/tableforos.html", {"forosdata":foros})

def vista_particiforo(request, id_foro):
    try:
        foroact = get_object_or_404(Foro, idforo=id_foro)
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar participar en el foro. Ese registro no existe")
        return redirect('url_foro')    
    comentarios = foroact.comentarios.all()
    if not comentarios:
        messages.add_message(request=request, level=messages.SUCCESS, message="Aún no hay intervenciones publicadas en este foro. Sea la primera persona en responder")
    comentarioform = ComentForm()
    respcomentario = ComentReply.objects.all()
    respcomentarioform = ReplyComentForm()
    return render(request, "psigcred/particiforo.html", {"forodata":foroact, "comentform":comentarioform, "comentdata":comentarios, "replyform":respcomentarioform, "replydata":respcomentario})

def vista_adicoment(request, id_foro):
    try:
        foroact = get_object_or_404(Foro, idforo=id_foro)
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar enviar comentario en el foro. Ese registro no existe")
        return redirect('url_particiforo')    
    if request.method == 'POST':
        comentarioform = ComentForm(request.POST)
        usucoment = get_object_or_404(Usuario, pk=request.user.pk)
        preform = comentarioform.save(commit=False)
        preform.forodebate = foroact
        preform.comentautor = usucoment
        try:
            preform.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="El comentario se publicó de manera exitosa")
        except:
            messages.add_message(request=request, level=messages.ERROR, message="No se pudo publicar el comentario por error en el sistema")
    return redirect('url_particiforo', id_foro)

def vista_replycoment(request, id_coment):
    try:
        comentact = get_object_or_404(ComentPost, idcoment=id_coment)
    except: 
        return redirect('url_particiforo')
    if comentact:
        replydatalist = ComentReply.objects.filter(comentforo = id_coment)
    return(request, "replycomentlist.html",{"replydata":replydatalist})

def vista_adireplycoment(request, id_coment):
    try:
        comentact = get_object_or_404(ComentPost, idcoment=id_coment)
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar enviar respuesta al comentario. Ese registro no existe")
        return redirect('url_particiforo')    
    if request.method == 'POST':
        replycomentform = ReplyComentForm(request.POST)
        usuresp = get_object_or_404(Usuario, pk=request.user.pk)
        preform = replycomentform.save(commit=False)
        preform.comentforo = comentact
        preform.replyautor = usuresp
        try:
            preform.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="La respuesta se publicó de manera exitosa")
        except:
            messages.add_message(request=request, level=messages.ERROR, message="No se pudo publicar la respuesta por error en el sistema")
    return redirect('url_particiforo', comentact.forodebate_id)


def vista_demanda(request):
    demandaform = DemandaForm()
    if request.POST:
        demandaform=DemandaForm(request.POST)
        if demandaform.is_valid():
            nombrecontxt=" El usuario " 
            areaconoctxt = request.POST.get("areaconoc")
            contenidocont=request.POST.get("descripcion")
            email_from = settings.EMAIL_HOST_USER
            buzon_destino=["carlosap@uclv.edu.cu"]
            enviado=False    
            #emailcontacto=EmailMessage("Mensaje desde la plataforma PSIGC","El usuario {} con nombre {} y correo electrónico {} envió este mensaje de contacto:\n\n {}".format(nombrecont,ecorreocont, contenidocont),"",["carlospm08@gmailcom"],reply_to=[ecorreocont])
            if areaconoctxt!='':
               # send_mail(areaconoctxt, contenidocont, contenidocont, buzon_destino,enviado,nombrecontxt)
               # emailcontacto.send()
               messages.add_message(request=request, level=messages.SUCCESS, message="La demanda ha sido enviada satisfactoriamente.")
               return redirect('url_demanda')
            else:
                messages.add_message(request=request, level=messages.ERROR, message="La demanda no pudo ser enviada por algú error del sistema")
    
    return render(request, "psigcred/demandForm.html", {'demform':demandaform})

