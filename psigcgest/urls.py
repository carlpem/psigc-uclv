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
from psigcgest import views

urlpatterns = [
    path('', views.vista_gestion, name='url_gestion'),
    path('url_noticiabd/', views.vista_noticiabd, name='url_noticiabd'),
    path('url_adinoticia/', views.vista_adinoticia, name='url_adinoticia'),
    path('url_edinoticia/<int:id_noti>', views.vista_edinoticia, name='url_edinoticia'),
    path('url_elinoticia/<int:id_noti>', views.vista_elinoticia, name='url_elinoticia'),

    path('url_eventobd/', views.vista_eventobd, name='url_eventobd'),
    path('url_adievento/', views.vista_adievento, name='url_adievento'),
    path('url_edievento/<int:id_event>', views.vista_edievento, name='url_edievento'),
    path('url_elievento/<int:id_event>', views.vista_elievento, name='url_elievento'),
    
    path('url_documentobd/', views.vista_documentobd, name='url_documentobd'),
    path('url_adidocumento/', views.vista_adidocumento, name='url_adidocumento'),
    path('url_edidocumento/<int:id_doc>', views.vista_edidocumento, name='url_edidocumento'),
    path('url_elidocumento/<int:id_doc>', views.vista_elidocumento, name='url_elidocumento'),


    path('url_forobd/', views.vista_forobd, name='url_forobd'),
    path('url_adiforo/', views.vista_adiforo, name='url_adiforo'),
    path('url_ediforo/<int:id_for>', views.vista_ediforo, name='url_ediforo'),
    path('url_eliforo/<int:id_for>', views.vista_eliforo, name='url_eliforo'),
    
    path('url_edicoment/', views.vista_edicoment, name='url_edicoment'),


    path('url_areaconocbd/', views.vista_areaconocbd, name='url_areaconocbd'),
    path('url_adiareaconoc/', views.vista_adiareaconoc, name='url_adiareaconoc'),
    path('url_ediareaconoc/<int:id_areacon>', views.vista_ediareaconoc, name='url_ediareaconoc'),
    path('url_eliareaconoc/<int:id_areacon>', views.vista_elimareaconoc, name='url_eliareaconoc'),

    path('url_expertosbd/', views.vista_expertosbd, name='url_expertosbd'),

    path('url_consultabd/', views.vista_consultabd, name='url_consultabd'),
    path('url_demandabd/', views.vista_demandabd, name='url_demandabd'),

]
