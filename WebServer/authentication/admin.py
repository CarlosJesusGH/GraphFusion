from .models import Feature, SampleNetwork, Description
from django.contrib import admin


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', "description", 'position', 'image',)
    # list_editable = ('position',)
    ordering = ('position',)


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('description', 'position',)
    ordering = ('position',)


@admin.register(SampleNetwork)
class SampleNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'network_file',)
    ordering = ('name',)