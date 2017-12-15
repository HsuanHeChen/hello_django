from django.shortcuts import render, redirect
# from django.core.exceptions import ValidationError
# from django.contrib import messages
from .models import List
from .forms import ItemForm


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, pk):
    _list = List.objects.get(id=pk)
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=_list)
            return redirect(_list)
    else:
        form = ItemForm()

    return render(request, 'lists/list.html', {'list': _list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)

    if form.is_valid():
        _list = List.objects.create()
        form.save(for_list=_list)
        return redirect(_list)
    else:
        return render(request, 'lists/home.html', {'form': form})
