from django.contrib import admin
from . import models


@admin.register(models.Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'type', 'dimensions')
    list_filter = ('name', 'manufacturer', 'type', 'publish')
    search_fields = ('name', 'manufacturer', 'dimensions')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('abbreviation', 'name', 'manufacturer', 'type', 'dimensions')


@admin.register(models.LogPModel)
class LogPModelAdmin(admin.ModelAdmin):
    list_display = ('column', 'eluent', 'gradient_time', 'k1', 'k2')
    list_filter = ('column', 'eluent', 'gradient_time')
    search_fields = ('column', 'eluent')
    ordering = ('column', 'eluent', 'gradient_time')
    prepopulated_fields = {'slug': ('column', 'eluent', 'gradient_time')}


@admin.register(models.LSERModel)
class LserModelAdmin(admin.ModelAdmin):
    list_display = ('column', 'eluent', 'gradient_time', 'k1', 'k2', 'k3', 'k4')
    list_filter = ('column', 'eluent', 'gradient_time')
    search_fields = ('column', 'eluent')
    ordering = ('column', 'eluent', 'gradient_time')
    prepopulated_fields = {'slug': ('column', 'eluent', 'gradient_time')}


@admin.register(models.Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'id')