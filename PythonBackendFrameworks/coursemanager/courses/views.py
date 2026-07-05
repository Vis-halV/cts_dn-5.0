from django.http import HttpResponse


def hello_view(request):
    """
    Simple function-based view.
    Returns a plain text response confirming the API is running.
    Called when a GET request hits /api/hello/
    """
    return HttpResponse('Course Management API is running')