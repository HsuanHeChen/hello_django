from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Union, Member
from .forms import UnionForm


# Create your views here.

class UnionList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Union


class UnionDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Union

    def get_context_data(self, **kwargs):
        context = super(UnionDetailView, self).get_context_data(**kwargs)
        context['members'] = Member.objects.filter(union_id=self.kwargs['pk'])
        return context


class UnionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Union
    form_class = UnionForm

    def form_valid(self, form):
        return super(UnionCreateView, self).form_valid(form)
