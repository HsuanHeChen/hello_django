from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Union, Member
from .forms import UnionForm


# Create your views here.

class UnionList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Union


class UnionDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Union

    def get_context_data(self, **kwargs):
        context = super(UnionDetail, self).get_context_data(**kwargs)
        context['members'] = Member.objects.filter(union_id=self.kwargs['pk'])
        return context


class UnionCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Union
    form_class = UnionForm

    def form_valid(self, form):
        response = super(UnionCreate, self).form_valid(form)
        # do something with self.object
        Member.objects.create(
            union_id=self.object.pk,
            user_id=self.request.user.pk,
            token='creater',
            join_at=timezone.now(),
            is_admin=True
        )
        return response


class UnionUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Union
    form_class = UnionForm
