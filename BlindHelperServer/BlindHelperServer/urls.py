"""BlindHelperServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from MouleOne import views as MouleOne
urlpatterns = [
    path('admin/', admin.site.urls),
    path('GetSpecifiedClassNews/', MouleOne.GetSpecifiedClassNews),
    path('GetSpecifiedNews/', MouleOne.GetSpecifiedNews),
    path("IdentifyText/",MouleOne.IdentifyText),
    path("IdentifyAudio/",MouleOne.IdentifyAudio),
    path("Search/",MouleOne.Search),
    path("GetNewsById/",MouleOne.GetNewsById),
    path("GetIndexNews/",MouleOne.GetIndexNews),
    path("",MouleOne.Index)
]
