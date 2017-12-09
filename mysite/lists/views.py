from django.shortcuts import render, redirect
from .models import Item

# Create your views here.


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/')

    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})