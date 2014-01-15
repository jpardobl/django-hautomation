from django.db import models
import simplejson

DEVICE_TYPES = ("switch", "dimmer")


class Protocol(models.Model):

    name = models.CharField(max_length=10, unique=True)
    gobj_name = models.CharField(max_length=10, unique=True)
    module = models.CharField(max_length=30, unique=True)
    validate_address_module = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.name

    def to_json(self):
        return simplejson.dumps({"name": self.name})


class Device(models.Model):
    caption = models.CharField(max_length=100)
    #device id
    did = models.CharField(max_length=100)
    status = models.IntegerField(blank=True, null=True)
    device_type = models.CharField(max_length=10, choices=(('switch', 'switch'), ('dimmer', 'dimmer'), ('sensor', 'sensor')))
    protocol = models.ForeignKey(Protocol, related_name="devices")

    def to_json(self):
        return simplejson.dumps({
            "caption": self.caption,
            "did": self.did,
            "status": self.status,
            "device_type": self.device_type,
            "protocol": self.protocol.__unicode__(),
            })

    def __unicode__(self):
        return "%s" % self.caption

    def cmd(self, cmd):
        pass

    class Meta:
        unique_together = ("protocol", "did")


import plugins

