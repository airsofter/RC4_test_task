from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'robot_serial')
    list_editable = ('customer', 'robot_serial')
    list_filter = ('customer', 'robot_serial')
    search_fields = ('customer', 'robot_serial')
