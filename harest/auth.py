from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from functools import wraps


def access_required(func, *args, **kwargs):
    print "hhh"

    def decorator(*args, **kwargs):
        print args[0].META
        for v in args[0].META:
            print "%s  \n" % v

        if "HTTP_USERNAME" not in args[0].META or "HTTP_PASSWORD" not in args[0].META:
            return HttpResponseForbidden()
        username = args[0].META["HTTP_USERNAME"]
        password = args[0].META["HTTP_PASSWORD"]
        user = authenticate(username=username, password=password)
        print "3"
        if user is not None:
            print "4"
            if user.is_active:
                print "5"

                return func(args[0], args, kwargs)
        return HttpResponseForbidden()

    return decorator
