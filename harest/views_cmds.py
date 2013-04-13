from hacore.models import Protocol, Device
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt

#
# Home automation commands
#
#   switch command
#      accepted values on|off


@csrf_exempt
def pl_switch(request, protocol, did):

    qd = QueryDict(request.body, request.encoding)
    if "value" not in qd:
        return HttpResponseBadRequest("Switch command needs a value to be set")
    value = qd["value"].lower()

    if value not in ("on", "off", "all"):
        return HttpResponseBadRequest("Switch command value not accepted!!")

    if request.method != "PUT":
        return HttpResponseBadRequest("Only PUT HTTP verb accepted for pl_switch command!!, arrived: %s" % request.method)

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="switch")

    exec "from %s import pl_switch" % protocol.module

    ret = pl_switch(device.did, value)

    return HttpResponse(status=200)


