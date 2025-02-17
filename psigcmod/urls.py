"""psigcproy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from psigcmod import views

urlpatterns = [
    path('',views.vista_basesdatos, name='url_basesdatos'),
    
    path('url_ejesbd/',views.vista_ejesbd, name='url_ejesbd'),
    path('url_adieje/', views.vista_adieje, name='url_adieje'),
    path('url_elieje/<int:id_eje>', views.vista_elieje, name='url_elieje'),
    path('url_ediejeinfo/<int:id_eje>', views.vista_ediejeinfo, name='url_ediejeinfo'),
        
    path('url_oacebd/', views.vista_oacebd, name='url_oacebd'),
    path('url_adioace/', views.vista_adioace, name='url_adioace'),
    path('url_edioace/<int:id_oace>', views.vista_edioace, name='url_edioace'),
    path('url_elioace/<int:id_oace>', views.vista_elioace, name='url_elioace'),

    path('url_progdesabd/', views.vista_progdesabd, name='url_progdesabd'),
    path('url_adiprogdesa/', views.vista_adiprogdesa, name='url_adiprogdesa'),
    path('url_ediprogdesa/<int:id_prog>', views.vista_ediprogdesa, name='url_ediprogdesa'),
    path('url_eliprogdesa/<int:id_prog>', views.vista_eliprogdesa, name='url_eliprogdesa'),

    path('url_entidactbd/', views.vista_entidactbd, name='url_entidactbd'),
    path('url_adientidact/', views.vista_adientidact, name='url_adientidact'),
    path('url_edientidact/<int:id_actor>', views.vista_edientidact, name='url_edientidact'),
    path('url_elientidact/<int:id_actor>', views.vista_elientidact, name='url_elientidact'),

    #path('url_proyinvestbd/', views.vista_proyinvestbd, name='url_proyinvestbd'),
    #path('url_adiproyinvest/', views.vista_adiproyinvest, name='url_adiproyinvest'),
    #path('url_ediproyinvest/<int:id_proy>', views.vista_ediproyinvest, name='url_ediproyinvest'),
    #path('url_eliproyinvest/<int:id_proy>', views.vista_eliproyinvest, name='url_eliproyinvest'),

    path('url_usuariobd/', views.vista_usuariobd, name='url_usuariobd'), 
    path('url_adiusuario/', views.vista_adiusuariobd, name='url_adiusuario'), 
    path('url_ediusuario/<int:id_usua>', views.vista_ediusuariobd, name='url_ediusuario'), 
    path('url_eliusuario/<int:id_usua>', views.vista_eliusuariobd, name='url_eliusuario'), 
    
]
