from django.http import HttpResponse


def health(request):
    """
    AWS healtcheck expects 200 status on root url
    """
    return HttpResponse('It\'s working ✨')
