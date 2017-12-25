from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin
# from django.core.exceptions import ValidationError
# from django.contrib import messages
from .models import List, Item
from .forms import ItemForm, ExistingListItemForm, NewListForm
from django.urls import reverse

User = get_user_model()


# def home_page(request):
#     return render(request, 'lists/home.html', {'form': ItemForm()})
class HomePageView(FormView):
    template_name = 'lists/home.html'
    form_class = ItemForm


def view_list(request, pk):
    _list = List.objects.get(id=pk)
    form = ExistingListItemForm(for_list=_list)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(_list)

    return render(request, 'lists/list.html', {'list': _list, 'form': form})


class ViewAndAddToList(DetailView, SingleObjectMixin):
    model = List
    template_name = 'lists/list.html'
    form_class = ExistingListItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form(ExistingListItemForm)
        return context

    def get_form(self, form_class):
        self.object = self.get_object()
        if self.request.method == 'POST':
            return form_class(for_list=self.object, data=self.request.POST)
        else:
            return form_class(for_list=self.object)


def my_lists(request, pk):
    owner = User.objects.get(id=pk)
    return render(request, 'lists/my_lists.html', {'owner': owner})


# it's only in test now.
def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        _list = form.save(owner=request.user)
        return redirect(_list)
    return render(request, 'lists/home.html', {'form': form})


class NewListView(CreateView):
    template_name = 'lists/home.html'
    form_class = ItemForm

    def form_valid(self, form):
        _list = List.objects.create()
        Item.objects.create(text=form.cleaned_data['text'], list=_list)
        return redirect(_list)
