from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, pk):
    _list = List.objects.get(id=pk)

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=_list)
            item.full_clean()
            item.save()
            return redirect(_list)
        except ValidationError:
            messages.add_message(request, messages.WARNING, 'You cannot have an empty list item.')

    return render(request, 'lists/list.html', {'list': _list})


def new_list(request):
    _list = List.objects.create()
    item = Item(text=request.POST['item_text'], list=_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        _list.delete()
        messages.add_message(request, messages.WARNING, 'You cannot have an empty list item.')
        return render(request, 'lists/home.html')

    return redirect(_list)
