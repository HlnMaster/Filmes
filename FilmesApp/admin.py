from django.contrib import admin
from .models import Genero, Filme, Avaliacao
# Register your models here.



class FilmeAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'genero', 'ano_lancamento']
    list_filter = ['genero', 'ano_lancamento']
    search_fields = ['titulo']

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'filme', 'nome', 'nota', 'data_criacao']
    list_filter = ['nota', 'filme']

admin.site.register(Genero)
admin.site.register(Filme, FilmeAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)