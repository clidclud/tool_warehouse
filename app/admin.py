from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import App

class AppAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nomenclature', 'unit', 'quantity')
    search_fields = ('nomenclature',)
    list_filter = ('unit',)

admin.site.register(App, AppAdmin)