from django.contrib import admin
 
from .models import ProgDesarrollo, AreaConocimiento,  Usuario, Grupo, ContactoBD, DemandaBD, Provincia, Municipio, ContactoBD
from .models import Oace, EntidActor, Publicacion, Noticia, Evento, Documento, Foro, ComentPost, ComentReply, InfoEjes

# , RecEstructural, RecGestProy, RecRelacional


class UsuarioAdmin(admin.ModelAdmin):
   readonly_fields=['ingreso',]

class ProvinciaAdmin(admin.ModelAdmin):
   search_fields = ['nombreprov']

class MunicipioAdmin(admin.ModelAdmin):
   search_fields = ['nombremuni']

class ContactoBDAdmin(admin.ModelAdmin):
   autocomplete_fields = ['municipio']


# Register your models here.

#admin.site.register(PerfilUsuario)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Grupo)
admin.site.register(InfoEjes)

admin.site.register(Oace)
admin.site.register(EntidActor)
admin.site.register(ProgDesarrollo)
admin.site.register(AreaConocimiento)

admin.site.register(ContactoBD, ContactoBDAdmin)

admin.site.register(DemandaBD)

admin.site.register(Publicacion)
admin.site.register(Noticia)
admin.site.register(Evento)
admin.site.register(Documento)
admin.site.register(Foro)
admin.site.register(ComentPost)
admin.site.register(ComentReply)

