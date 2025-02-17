"""sigcsanproy URL Configuration

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
from psigcred import views

urlpatterns = [
    path('',views.vista_redconoc, name='url_redconoc'),
    
    path('url_noticia/', views.vista_noticia, name='url_noticia'),
    path('url_leernoticia/<int:id_post>', views.vista_leernoticia, name='url_leernoticia'),

    path('url_evento/', views.vista_evento, name='url_evento'),
    
    path('url_foro/', views.vista_foro, name='url_foro'),
    path('url_particiforo/<int:id_foro>', views.vista_particiforo, name='url_particiforo'),
    path('url_adicoment/<int:id_foro>', views.vista_adicoment, name='url_adicoment'),
    path('url_adireplycoment/<int:id_coment>', views.vista_adireplycoment, name='url_adireplycoment'),


    path('url_documento/', views.vista_documento, name='url_documento'),
    
    path('url_areasconoc/',views.vista_areasconoc, name='url_areasconoc'),
    path('url_expertos/',views.vista_expertos, name='url_expertos'),
    
    path('url_demanda/',views.vista_demanda, name='url_demanda'),
    path('url_envdemanda/',views.vista_demanda, name='url_envdemanda'),
]
