"""florarie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from django.http import HttpResponse
from produse import views as pv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pv.index, name='index'),
    path('plante/', pv.plante_lista, name='plante'),
    path('plante/<slug:produs_nume>/<int:produs_id>/', pv.detaliu_planta, name='planta'),
    path('plante/categorie/<slug:categorie_nume>/<int:cat_id>/', pv.categorie, name='categorie'),
    path('contact/', pv.contact, name='contact'),
    path('autentificare/', pv.login, name='autentificare'),
    path('cont/', pv.cont, name='cont'),
    path('logout/', pv.logout, name='logout'),
    path('cos/', pv.cos, name='cos'),
    path('adauga_cos/<int:produs_id>/<int:cantitate>/', pv.adauga_in_cos,
         name='adauga_cos'),
    path('stergere_produs/<int:produs_id>/', pv.stergere_produs_cos,
         name='stergere_produs'),
    path('plata/', pv.plata, name='plata'),
    path('comanda/', pv.comanda, name='comanda'),
    path('detaliu-comanda/<slug:referinta>/', pv.detaliu_comanda,
         name='detaliu_comanda'),
]
