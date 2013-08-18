from hacore.models import Protocol
from django.shortcuts import render_to_response
from auth import access_required


def get(request, *args, **kwargs):

    data = [x.to_json() for x in Protocol.objects.all()]

    response = render_to_response(
        "device/list.json",
        {"data": data},
        content_type="application/json",
    )

    response['Cache-Control'] = 'no-cache'
    return response


@access_required
def entrance(request, *args, **kwargs):

    if request.method == "GET":
        return get(request, *args, **kwargs)

    return HttpResponseBadRequest(simplejson.dumps({"errors": ["Only GET HTTP verb accepted for Protocol resources"]}))
