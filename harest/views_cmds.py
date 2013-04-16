from hacore.models import Protocol, Device
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from auth import access_required
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
        return HttpResponseBadRequest("Switch command needs a value to be set")
    value = qd["value"].lower()

    if request.method != "PUT":
        return HttpResponseBadRequest("Only PUT HTTP verb accepted for pl_switch command!!, arrived: %s" % request.method)

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did)

    exec "from %s import pl_switch" % protocol.module

    try:
        ret = pl_switch(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(ex.message)

    return HttpResponse(status=200)


@csrf_exempt
@access_required
def pl_dim(request, protocol, did):

    if "value" not in request.POST:
        return HttpResponseBadRequest("Dim command needs a value to be set")
    value = request.POST["value"]

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST(no idempotent) HTTP verb accepted for pl_dim command!!, arrived: %s" % request.method)

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="dimmer")

    exec "from %s import pl_dim" % protocol.module
    try:
        ret = pl_dim(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(ex.message)

    return HttpResponse(status=200)


@csrf_exempt
@access_required
def pl_bri(request, protocol, did):

    if "value" not in request.POST:
        return HttpResponseBadRequest("Bri command needs a value to be set")
    value = request.POST["value"]

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST(no idempotent) HTTP verb accepted for pl_bri command!!, arrived: %s" % request.method)

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="dimmer")

    exec "from %s import pl_bri" % protocol.module
    try:
        ret = pl_bri(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(ex.message)

    return HttpResponse(status=200)
