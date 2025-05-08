from django.contrib import admin
from .models import TODO

# Register your models here.
@admin.register(TODO)
class TODOAdmin(admin.ModelAdmin):
    pass