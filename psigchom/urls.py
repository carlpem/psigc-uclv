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
from psigchom import views
from .views import vista_contacto, vista_loginUser, vista_registUser, vista_getmunics, vista_proceden

urlpatterns = [
    path('',views.vista_inicio, name='url_inicio'),
    path('url_ayuda/', views.vista_codayuda, name='url_ayuda'),
    path('url_codigo/', views.vista_codayuda, name='url_codigo'),
    path('url_registuser/',vista_registUser.as_view(), name='url_registuser'),
    path('url_loginuser/', views.vista_loginUser, name='url_loginuser'),
    path('url_sideloginuser/', views.sidelogin_form, name='url_sideloginuser'),
    
    path('url_perfiluser/<int:id_user>', views.vista_PerfilUser, name='url_perfiluser'),
    path('url_updperfuser/', views.vista_PerfilUser, name='url_updperfuser'),

    path('url_logout/', views.vista_LogoutUser, name='url_logout'),
    path('url_contacto/', vista_contacto.as_view(), name='url_contacto'),

    path('url_proceden/', views.vista_proceden, name='url_proceden'),
    path('url_getmunics/', views.vista_getmunics, name='url_getmunics'),
]
