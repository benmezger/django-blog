from django.conf import settings


class SetContextObjectNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        response.context_data["author_info"] = settings.AUTHOR_INFO
        response.context_data["site"] = settings.SITE_INFO

        return response
