from hacore.models import Protocol, Device
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from auth import access_required
from django.core.urlresolvers import reverse
import simplejson


@csrf_exempt
@access_required
def pl_all_lights_on(request, protocol, group):
    if request.method != "PUT":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only PUT HTTP verb accepted for pl_all_lights_on command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )
    try:
        protocol = Protocol.objects.get(name=protocol)
    except Protocol.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Protocol %s not found" % protocol, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching protocol %s: %s" % (protocol, er), ]}),
            content_type="application/json",
            )

    # ginsfsm ***********************************
    from ginsfsm.globals import global_get_gobj
    driver = global_get_gobj(protocol.gobj_name, protocol.name)
    driver.post_event(
        driver,
        "EV_COMMAND",
        data=simplejson.dumps({
            "cmd": "pl_all_lights_on",
            "group": group,
        }))

    # ginsfsm ***********************************

    #TODO changes in device must be made from EV_DEVICE_UPDATE
    for device in Device.objects.filter(did__istartswith=group):
        device.status = 100
        device.save()
    response = HttpResponse(simplejson.dumps({"status": "ok"}))
    response.content_type = "application/json"
    return response


@csrf_exempt
@access_required
def pl_all_lights_off(request, protocol, group):
    if request.method != "PUT":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only PUT HTTP verb accepted for pl_all_lights_off command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )
    try:
        protocol = Protocol.objects.get(name=protocol)
    except Protocol.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Protocol %s not found" % protocol, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching protocol %s: %s" % (protocol, er), ]}),
            content_type="application/json",
            )

    # ginsfsm ***********************************
    from ginsfsm.globals import global_get_gobj
    driver = global_get_gobj(protocol.gobj_name, protocol.name)
    driver.post_event(
        driver,
        "EV_COMMAND",
        data=simplejson.dumps({
            "cmd": "pl_all_lights_off",
            "group": group,
        }))

    # ginsfsm ***********************************

    #TODO changes in device must be made from EV_DEVICE_UPDATE
    for device in Device.objects.filter(did__istartswith=group):
        device.status = 0
        device.save()
    response = HttpResponse(simplejson.dumps({"status": "ok"}))
    response.content_type = "application/json"
    return response


@csrf_exempt
@access_required
def pl_switch(request, protocol, did):

    if request.method != "PUT":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only PUT HTTP verb accepted for pl_switch command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )

    qd = QueryDict(request.body, request.encoding)
    if "value" not in qd:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Switch command needs a value to be set", ]}),
            content_type="application/json",
            )
    value = qd["value"].lower()

    try:
        protocol = Protocol.objects.get(name=protocol)
    except Protocol.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Protocol %s not found" % protocol, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching protocol %s: %s" % (protocol, er), ]}),
            content_type="application/json",
            )

    try:
        device = Device.objects.get(did=did)
    except Device.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Device (did=%s) not found" % did, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching device (did=%s): %s" % (did, er), ]}),
            content_type="application/json",
            )

    # ginsfsm ***********************************
    from ginsfsm.globals import global_get_gobj
    driver = global_get_gobj(protocol.gobj_name, protocol.name)
    driver.post_event(
        driver,
        "EV_COMMAND",
        data=simplejson.dumps({
            "cmd": "pl_switch",
            "did": device.did,
            "value": value,
        }))

    # ginsfsm ***********************************
    """
    exec "from %s.cmds import pl_switch" % protocol.module

    try:
        ret = pl_switch(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )
    """
    #TODO changes in device must be made from EV_DEVICE_UPDATE
    device.status = 0 if value == "off" else 100
    device.save()
    response = redirect(reverse('device_by_id', kwargs={"protocol": device.protocol, "did": device.did}))
    response.content_type = "application/json"
    return response


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
            content_type="application/json", )
    value = request.POST["value"]

    try:
        protocol = Protocol.objects.get(name=protocol)
    except Protocol.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Protocol %s not found" % protocol, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching protocol %s: %s" % (protocol, er), ]}),
            content_type="application/json",
            )

    try:
        device = Device.objects.get(did=did, device_type="dimmer")
    except Device.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Device (did=%s, type=dimmer) not found" % did, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching device (did=%s, type=dimmer): %s" % (did, er), ]}),
            content_type="application/json",
            )

    # ginsfsm ***********************************
    from ginsfsm.globals import global_get_gobj
    driver = global_get_gobj(protocol.gobj_name, protocol.name)
    driver.post_event(
        driver,
        "EV_COMMAND",
        data=simplejson.dumps({
            "cmd": "pl_dim",
            "did": device.did,
            "value": value,
        }))

    # ginsfsm ***********************************

    device.status = 0 if value == "off" else 100
    device.save()
    response = redirect(reverse('device_by_id', kwargs={"protocol": device.protocol, "did": device.did}))
    response.content_type = "application/json"
    return response


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

    try:
        protocol = Protocol.objects.get(name=protocol)
    except Protocol.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Protocol %s not found" % protocol, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching protocol %s: %s" % (protocol, er), ]}),
            content_type="application/json",
            )

    try:
        device = Device.objects.get(did=did, device_type="dimmer")
    except Device.DoesNotExist:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Device (did=%s, type=dimmer) not found" % did, ]}),
            content_type="application/json",
            )
    except Exception, er:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error while fetching device (did=%s, type=dimmer): %s" % (did, er), ]}),
            content_type="application/json",
            )


    # ginsfsm ***********************************
    from ginsfsm.globals import global_get_gobj
    driver = global_get_gobj(protocol.gobj_name, protocol.name)
    driver.post_event(
        driver,
        "EV_COMMAND",
        data=simplejson.dumps({
            "cmd": "pl_bri",
            "did": device.did,
            "value": value,
        }))

    # ginsfsm ***********************************

    device.status = 0 if value == "off" else 100
    device.save()
    response = redirect(reverse('device_by_id', kwargs={"protocol": device.protocol, "did": device.did}))
    response.content_type = "application/json"
    return response
