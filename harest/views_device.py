from django.http import HttpResponseBadRequest, HttpResponse
from hacore.models import Device, Protocol
from forms import DeviceForm
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import simplejson
from django.db import IntegrityError


def get(request, *args, **kwargs):

    if "did" in kwargs:
        obj = get_object_or_404(Device, id=kwargs["did"])

        response = HttpResponse(
            content=obj.to_json(),
            content_type="application/json",
        )

        response['Cache-Control'] = 'no-cache'
        return response

    if "protocol" in request.GET:
        if request.GET["protocol"] == "" or request.GET["protocol"] is None:
            return HttpResponseBadRequest("Invalid protocol")
        protocol = get_object_or_404(Protocol, name=request.GET["protocol"])

        data = [x.to_json() for x in protocol.devices]

    elif "device_type" in request.GET:
        if request.GET["device_type"] == "" or request.GET["device_type"] is None:
            return HttpResponseBaRequest("Invalid device_type")

        data = [x.to_json() for x in Device.objects.filter(device_type=request.GET["device_type"])]

    elif "status" in request.GET:
        if request.GET["status"] == "" or request.GET["status"] is None:
            return HttpResponseBadRequest("Ivalid status")

        data = [x.to_json() for x in Device.objects.filter(status=request.GET["status"])]

    else:
        return HttpResponseBadRequest(
            "Posible mandatory query filters 'did' or 'protocol' or 'device_type' or 'status'")
    response = render_to_response(
        "device/list.json",
        {"data": data},
        content_type="application/json",
    )
    response['Cache-Control'] = 'no-cache'
    return response


def put(request, did):
    obj = get_object_or_404(Device, did=did)
    form = DeviceForm(request.POST, instance=obj)
    if form.is_valid():

        obj = form.save(commit=False)
        if "protocol" in request.POST:
            protocol = get_object_or_404(Protocol, name=request.POST["protocol"])
            obj.protocol = protocol
        obj.save()

        return redirect(reverse('device_by_id', args=[obj.id]))
    return HttpResponseBadRequest(simplejson.dumps({"errors": [x for x in form.errors]}))


def delete(request, did):
    get_object_or_404(Device, did=did).delete()
    return HttpResponse(status=204)


def post(request):

    if "protocol" not in request.POST:
        return HttpResponseBadRequest(simplejson.dumps({"errors": ["protocol"]}))
    protocol = get_object_or_404(Protocol, name=request.POST["protocol"])

    form = DeviceForm(request.POST)
    if form.is_valid():
        exec "from %s import validate_address" % protocol.validate_address_module
        obj = form.save(commit=False)
        obj.protocol = protocol
        try:
            validate_address(obj.did)
            obj.save()
        except ValueError:
            return HttpResponseBadRequest({"errors": ["did"]})
        except IntegrityError:
            return HttpResponse(
                status=409,
                content=simplejson.dumps({"conflicting": ["did", "protocol"]})
                )
        return redirect(reverse('device_by_id', args=[obj.id]))
    return HttpResponseBadRequest(simplejson.dumps({"errors": [x for x in form.errors]}))


@csrf_exempt
def entrance(request, *args, **kwargs):

    if request.method == "GET":
        return get(request, *args, **kwargs)

    if request.method == "PUT":
        try:
            did = kwargs["did"]
            return put(request, did)
        except KeyError:
            return HttpResponseBadRequest("Device id is missing")

        return put(request)

    if request.method == "DELETE":
        try:
            did = kwargs["did"]
            return delete(request, did)
        except KeyError:
            return HttpResponseBadRequest("Device id is missing")

    if request.method == "POST":
        return post(request)
