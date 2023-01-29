from django.contrib import admin
from produse.models import Categorii, Produse, Promotii, Poze, Useri, Comenzi

class CategoriiAdmin(admin.ModelAdmin):
    list_display = ['nume','poza']
    search_fields = ['nume']
    ordering = ['nume']

class ProduseAdmin(admin.ModelAdmin):
    list_display = ['nume','categorie','pret','stoc']
    search_fields = ['nume']
    list_filter = ['categorie']
    
class PromotiiAdmin(admin.ModelAdmin):
    list_display = ['pret_redus','procent','data_inceput','data_sfarsit']

class UseriAdmin(admin.ModelAdmin):
    list_display = ['user','adresare','prenume','nume','email']

class ComenziAdmin(admin.ModelAdmin):
    list_display = ['referinta','platita','livrata']

admin.site.register(Categorii, CategoriiAdmin)
admin.site.register(Produse, ProduseAdmin)
admin.site.register(Promotii, PromotiiAdmin)
admin.site.register(Useri, UseriAdmin)
admin.site.register(Comenzi, ComenziAdmin)
