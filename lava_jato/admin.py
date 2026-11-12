from django.contrib import admin

from lava_jato.models import Lavagem

# Register your models here.
admin.site.register(Lavagem)
class LavagemAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'data_hora', 'valor')
    list_filter = ('data_hora',)
    search_fields = ('veiculo',)