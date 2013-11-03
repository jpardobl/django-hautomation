from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from functools import wraps
import simplejson


def access_required(func, *args, **kwargs):

    def decorator(*args, **kwargs):
        if "HTTP_USERNAME" not in args[0].META or "HTTP_PASSWORD" not in args[0].META:
            return HttpResponseForbidden(
                simplejson.dumps({"errors": ["HTTP_USERNAME or HTTP_PASSWORD headers not sent", ]}),
                content_type="application/json",)

        username = args[0].META["HTTP_USERNAME"]
        password = args[0].META["HTTP_PASSWORD"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                return func(*args, **kwargs)
        return HttpResponseForbidden(
            simplejson.dumps({"errors": ["username/password not valid", ]}),
            content_type="application/json",)

    return decorator
