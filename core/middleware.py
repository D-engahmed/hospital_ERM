import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class HospitalContextMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            response.context_data['current_year'] = datetime.now().year
            response.context_data['app_name'] = 'Hospital ERM'
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._request_start_time = datetime.now()

    def process_response(self, request, response):
        if hasattr(request, '_request_start_time'):
            duration = (datetime.now() - request._request_start_time).total_seconds()
            if duration > 1.0:
                logger.warning(
                    f'Slow request: {request.method} {request.path} took {duration:.2f}s'
                )
        return response
