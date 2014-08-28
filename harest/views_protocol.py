from hacore.models import Protocol
from django.shortcuts import render_to_response
from auth import access_required
from django.http import HttpResponseBadRequest
import simplejson
import logging
from django.conf import settings


logger = logging.getLogger("rest")
logger.setLevel(settings.LOG_LEVEL)


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

    try:
        if request.method == "GET":
            return get(request, *args, **kwargs)

        return HttpResponseBadRequest(simplejson.dumps({"errors": ["Only GET HTTP verb accepted for Protocol resources"]}))
    except Exception as ex:
        logger.error(ex)
        raise ex