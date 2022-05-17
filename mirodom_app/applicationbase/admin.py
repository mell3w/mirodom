from django.contrib import admin
from .models import Appliactions, Masters, Warehouse, Fine
from applicationbase.models import AdvUser
from .models import SuperRubric, SubRubric
from .models import AdditionalImage

class SubRubricInline(admin.TabularInline):
    model=SubRubric



class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage

class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ['city','address', 'reason_for_calling','master']
    list_display_links = ['address', 'reason_for_calling','master']
    fields = ('master','city','address','flat','full_name_client', 'reason_for_calling','treaty','door_closer','img_door_closer','monetary','sum','premium','fine',
              'choose_fine','comment','status','calcucalted')
    search_fields = ('city','address', 'reason_for_calling', 'comment',)
    inlines = (AdditionalImageInline,)


# Register your models here.
class MastersAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    list_display_links = ['full_name']
    search_fields = ('full_name',)

class FineAdmin(admin.ModelAdmin):
    list_display = ['reason']
    list_display_links = ['reason']
    search_fields = ('reason','amount')

admin.site.register(Appliactions, ApplicationsAdmin)
admin.site.register(Masters, MastersAdmin)
admin.site.register(Warehouse)
admin.site.register(Fine, FineAdmin)
admin.site.register(AdvUser)