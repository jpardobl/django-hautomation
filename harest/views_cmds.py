from hacore.models import Protocol, Device
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from auth import access_required
import simplejson
#
# Home automation commands
#
#   switch command
#      accepted values on|off



@csrf_exempt
@access_required
def pl_switch(request, protocol, did):

    qd = QueryDict(request.body, request.encoding)
    if "value" not in qd:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Switch command needs a value to be set", ]}),
            content_type="application/json",
            )
    value = qd["value"].lower()

    if request.method != "PUT":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only PUT HTTP verb accepted for pl_switch command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )

    print "protocol: %s" % protocol
    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, protocol=protocol, did=did)

    exec "from %s import pl_switch" % protocol.module

    try:
        ret = pl_switch(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )

    device.status = 0 if value == "off" else 100
    device.save()
    return HttpResponse(status=200, content_type="application/json")


@csrf_exempt
@access_required
def pl_dim(request, protocol, did):

    if request.method != "POST":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only POST(no idempotent) HTTP verb accepted for pl_dim command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )

    if "value" not in request.POST:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Dim command needs a value to be set", ]}),
            content_type="application/json",
            )
    value = request.POST["value"]

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="dimmer")
    print "sending a value of: %s" % value
    exec "from %s import pl_dim" % protocol.module
    try:
        ret = pl_dim(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )

    ds = int(device.status) - int(value)
    if ds < 0:
        ds = 0
    device.status = ds
    device.save()
    return HttpResponse(status=200,
            content_type="application/json",
            )


@csrf_exempt
@access_required
def pl_bri(request, protocol, did):

    if request.method != "POST":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only POST(no idempotent) HTTP verb accepted for pl_bri command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )
    if "value" not in request.POST:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Bri command needs a value to be set", ]}),
            content_type="application/json",
            )
    value = request.POST["value"]

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="dimmer")

    exec "from %s import pl_bri" % protocol.module
    try:
        ret = pl_bri(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )

    ds = int(device.status) - int(value)
    if ds > 100:
        ds = 100
    device.status = ds
    device.save()
    return HttpResponse(
        status=200,
        content_type="application/json",
        )
