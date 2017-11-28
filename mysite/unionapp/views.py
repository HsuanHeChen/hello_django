from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Union, Member
from .forms import UnionForm


# Create your views here.

class UnionList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Union


class UnionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Union
    form_class = UnionForm

    def form_valid(self, form):
        return super(UnionCreateView, self).form_valid(form)
