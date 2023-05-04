from django.contrib import admin
from .models import SoEmployee, SoOut, SoType, Shift
# Register your models here.



admin.site.register(SoEmployee)
admin.site.register(SoOut) 
admin.site.register(Shift)
