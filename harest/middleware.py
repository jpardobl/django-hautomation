from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
import simplejson, logging, traceback

from django.conf import settings

logger = logging.getLogger("rest")
logger.setLevel(settings.LOG_LEVEL)


class Exception2Json():
    """
    Middleware meant to process exception found at views
    """
    def process_exception(self, request, exception):
        logger.error(exception)
        if isinstance(exception, Http404):
            return HttpResponseNotFound(
                content=simplejson.dumps({"errors": [str(exception)]}),
                content_type="application/json",)

        logger.error(traceback.format_exc())
        return HttpResponseServerError(
            content=simplejson.dumps({"errors": ["Server error", ]}),
            content_type="application/json",)
