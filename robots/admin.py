from django.contrib import admin

from .models import Robot, RobotModel


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial', 'model', 'version', 'created')
    list_editable = ('model', 'version', 'created')
    list_filter = ('model', 'version', 'created')
    search_fields = ('serial', 'model', 'version', 'created')

    def serial(self, obj):
        return f'{obj.model}-{obj.version}'


@admin.register(RobotModel)
class RobotModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_editable = ('name',)
