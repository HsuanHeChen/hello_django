from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def hello_world(request, name = ""):
    if (name == ""):
        current_time = datetime.now()
        return render(request, 'hello_world.html', locals())
    else:
        return HttpResponse("Hello world! {}!".format(name))
