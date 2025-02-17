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
from psigcrep import views

urlpatterns = [
    path('',views.vista_reportes, name='url_reportes'),
    path('url_general/', views.vista_generalidad, name='url_general'),

    path('url_indentidactreg/', views.vista_reg_entidactores, name='url_indentidactreg'),
    path('url_evalentidactreg/', views.vista_reg_entidactores, name='url_evalentidactreg'),
    path('url_regentimunic/<int:id_entid>/<int:id_munic>', views.vista_regentimunic, name='url_regentimunic'),

    path('url_indicadores/<int:id_entidact>/<int:id_mun>', views.vista_indicadores, name='url_indicadores'),
    path('url_evaluaciones/<int:id_entidact>/<int:id_mun>', views.vista_evaluaciones, name='url_evaluaciones'),

    path('url_conocasist/', views.vista_conocasist, name='url_conocasist'),
        
    
]
