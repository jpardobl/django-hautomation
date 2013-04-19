from django.forms import ModelForm
from hacore.models import Device
from django.core.exceptions import ValidationError
from django.forms.fields import FileField


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ["protocol"]


class DeviceUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceUpdateForm, self).__init__(*args, **kwargs)
        self.fields["device_type"].required = False
        self.fields["caption"].required = False

    class Meta:
        model = Device
        exclude = ["did", "status", "protocol"]
