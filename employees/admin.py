from django.contrib import admin
from .models import SoEmployee, SoOut, SoType, Shift
# Register your models here.


 
admin.site.register(Shift)

admin.site.register(SoType)


@admin.register(SoOut)
class SoOutAdmin(admin.ModelAdmin): 
    list_display = ['co_fk_em_id_key', 'co_fk_type_id_key', 'co_date', 'co_time_arrived', 'co_time_dif']
    list_filter = ('co_fk_em_id_key', 'co_fk_type_id_key', 'co_date', 'co_time_arrived', 'co_time_dif')
    search_fields = ('co_fk_em_id_key', 'co_fk_type_id_key', 'co_date', 'co_time_arrived', 'co_time_dif')
    ordering = ('co_fk_type_id_key',) 
    list_per_page = 35 
    actions = ['my_custom_action']
    def my_custom_action(self, request, queryset):
        print("sfsds test")
        self.message_user(request, "Selected records have been deleted.")
    my_custom_action.short_description = "testit"
         

    fieldsets = (
        ('Employee', {
            'fields': ('co_fk_em_id_key', 'co_fk_type_id_key', 'co_date','co_time_arrived')
        }),
    )
 

@admin.register(SoEmployee)
class SoEmployeeAdmin(admin.ModelAdmin):
    list_display = ('em_name', 'em_zone')
    list_filter = ('em_zone',)
    search_fields = ('em_name',)
    ordering = ('em_name',)
    list_per_page = 33
    fieldsets = (
        ('Employee', {
            'fields': ('em_name', 'em_zone')
        }),
    )
    def get_ordering(self, request):
        return ['em_name']
