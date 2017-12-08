from django.http import HttpResponse
# from .models import List

# Create your views here.


def home_page(request):
    return HttpResponse('<html><title>TODO</title></html>')
