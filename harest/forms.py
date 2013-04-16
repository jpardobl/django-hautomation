from django.forms import ModelForm
from hacore.models import Device


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ["protocol"]


class DeviceUpdateForm(ModelForm):
    class Meta:
        model = Device
        exclude = ["did"]
