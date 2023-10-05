from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email')
    list_editable = ('email',)
    list_filter = ('email',)
    search_fields = ('email',)
