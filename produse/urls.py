from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from produse import views as pv

urlpatterns = [
    path('', pv.index, name='index'),
    path('entry/<int:produs_id>/', pv.entry_detail, name='entry'),
]
