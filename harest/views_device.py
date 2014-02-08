from django.http import HttpResponseBadRequest, HttpResponse
from hacore.models import Device, Protocol
from forms import DeviceForm, DeviceUpdateForm
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import simplejson, logging
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from auth import access_required
from django.http import QueryDict

#@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Alumnos presenciales').exists())
def get(request, *args, **kwargs):
    try:
        if "did" in kwargs and "protocol" in kwargs:
            protocol = get_object_or_404(Protocol, name=kwargs["protocol"])
            obj = get_object_or_404(Device, protocol=protocol, did=kwargs["did"])
    
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
    
            data = [x.to_json() for x in protocol.devices.all()]
    
        elif "device_type" in request.GET:
            if request.GET["device_type"] == "" or request.GET["device_type"] is None:
                raise Exception("Invalid device_type")
    
            data = [x.to_json() for x in Device.objects.filter(device_type=request.GET["device_type"])]
    
        elif "status" in request.GET:
            if request.GET["status"] is None:
                raise Exception("Invalid status")
    
            data = [x.to_json() for x in Device.objects.filter(status=request.GET["status"])]
    
        else:
            raise Exception("Posible mandatory query filters 'did' or 'protocol' or 'device_type' or 'status'")
                    
        response = render_to_response(
            "device/list.json",
            {"data": data},
            content_type="application/json",
        )
        response['Cache-Control'] = 'no-cache'
        return response
    except Exception, er:
        response =  HttpResponseBadRequest(
            content=simplejson.dumps({"errors": er}),
            content_type="application/json") 
        response['Cache-Control'] = 'no-cache'
        return response

def put(request, protocol, did):

    protocol = get_object_or_404(Protocol, name=protocol)
    obj = get_object_or_404(Device, protocol=protocol, did=did)

    qd = QueryDict(request.body, request.encoding)
    form = DeviceUpdateForm(qd, instance=obj)

    if form.is_valid():
        obj = form.save(commit=False)

        obj.save()

        response = redirect(reverse('device_by_id', kwargs={"protocol": obj.protocol, "did": obj.id}))
        response.content_type = "application/json"
        return response
    logging.debug("PUT view: errores en el form %s" % form.errors)
    return HttpResponseBadRequest(
        simplejson.dumps({"errors": [x for x in form.errors]}),
        content_type="application/json")


def delete(request, protocol, did):
    protocol = get_object_or_404(Protocol, name=protocol)
    get_object_or_404(Device, protocol=protocol, did=did).delete()
    return HttpResponse(status=204)


def post(request):

    if "protocol" not in request.POST:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["protocol"]}),
            content_type="application/json",
            )
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
            return HttpResponseBadRequest(
                content=simplejson.dumps({"errors": ["did"]}),
                content_type="application/json",
                )
        except IntegrityError:
            return HttpResponse(
                status=409,
                content=simplejson.dumps({"conflicting": ["did", "protocol"]}),
                content_type="application/json",
                )
        response = redirect(reverse('device_by_id', kwargs={"protocol": obj.protocol, "did": obj.id}))
        response.content_type = "application/json"
        return response
    return HttpResponseBadRequest(
        content=simplejson.dumps({"errors": [x for x in form.errors]}),
        content_type="application/json",)


@csrf_exempt
@access_required
def entrance(request, *args, **kwargs):

    if request.method == "GET":
        return get(request, *args, **kwargs)

    if request.method == "PUT":
        try:
            did = kwargs["did"]
            protocol = kwargs["protocol"]
            return put(request, protocol, did)
        except KeyError:
            return HttpResponseBadRequest(simplejson.dumps({"errors": ["Device id(did) or protocol missing"]}))

        return put(request)

    if request.method == "DELETE":
        try:
            did = kwargs["did"]
            protocol = kwargs["protocol"]
            return delete(request, protocol, did)
        except KeyError:
            return HttpResponseBadRequest(simplejson.dumps({"errors": ["Device id(did) or protocol missing"]}))

    if request.method == "POST":
        return post(request)
