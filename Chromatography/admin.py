from django.contrib import admin
from . import models


@admin.register(models.Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name', 'manufacturer', 'type', 'dimensions')
    list_filter = ('name', 'manufacturer', 'type', 'publish')
    search_fields = ('name', 'manufacturer', 'dimensions')
    prepopulated_fields = {'slug': ('abbreviation',)}
    ordering = ('abbreviation', 'name', 'manufacturer', 'type', 'dimensions')


@admin.register(models.Eluent)
class EluentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.ChromatographicModel)
class ChromatographicModelAdmin(admin.ModelAdmin):
    list_display = ('slug', 'column', 'eluent', 'k1', 'k2')
    list_filter = ('column', 'eluent')
    search_fields = ('column', 'eluent')
    ordering = ('column', 'eluent')
    prepopulated_fields = {'slug': ('column', 'eluent')}



