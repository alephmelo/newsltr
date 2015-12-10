from django.contrib import admin
from .models import Person

@admin.register(Person)
class PlayerAdmin(admin.ModelAdmin):
	list_display = ['name', 'email']