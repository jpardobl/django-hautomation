from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
import simplejson, logging, traceback

class Exception2Json():
    """
    Middleware meant to process exception found at views
    """

    def process_exception(self, request, exception):
        logging.debug("middleware.Exception2Json: %s" % exception)
        if isinstance(exception, Http404):
            return HttpResponseNotFound(
                content=simplejson.dumps({"errors": [str(exception)]}),
                content_type="application/json",)

        logging.debug("middleware.Exception2Json: %s " % traceback.format_exc())
        return HttpResponseServerError(
            content=simplejson.dumps({"errors": ["Server error", ]}),
            content_type="application/json",
        )
