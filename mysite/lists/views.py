from django.shortcuts import render, redirect
from .models import Item, List

# Create your views here.


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, pk):
    _list = List.objects.get(id=pk)
    return render(request, 'lists/list.html', {'list': _list})


def add_item(request, pk):
    _list = List.objects.get(id=pk)
    Item.objects.create(text=request.POST['item_text'], list=_list)
    return redirect('/lists/%d/' % (_list.id,))


def new_list(request):
    _list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=_list)
    return redirect('/lists/%d/' % (_list.id,))
