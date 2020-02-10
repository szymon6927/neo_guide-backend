from django.http import HttpResponse
from django.views import View


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        """
        AWS healtcheck expects 200 status on root url
        """
        return HttpResponse('It\'s working ✨')
