from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
# from django.contrib import messages
from .models import List
from .forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, pk):
    _list = List.objects.get(id=pk)
    form = ExistingListItemForm(for_list=_list)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(_list)

    return render(request, 'lists/list.html', {'list': _list, 'form': form})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        _list = form.save(owner=request.user)
        return redirect(_list)
    return render(request, 'lists/home.html', {'form': form})


def my_lists(request, pk):
    owner = User.objects.get(id=pk)
    return render(request, 'lists/my_lists.html', {'owner': owner})
