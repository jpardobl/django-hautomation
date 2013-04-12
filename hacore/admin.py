from django.contrib import admin
from models import *


class ProtocolAdmin(admin.ModelAdmin):
    pass
admin.site.register(Protocol, ProtocolAdmin)


class DeviceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Device, DeviceAdmin)
