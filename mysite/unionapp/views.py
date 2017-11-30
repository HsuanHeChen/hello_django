from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from .models import Union, Member
from .forms import UnionForm


# Create your views here.
class UnionMixin(object):
    login_url = '/login/'
    model = Union


class UnionList(LoginRequiredMixin, UnionMixin, ListView):
    
    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset
        queryset = super(UnionList, self).get_queryset()

        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # Return a filtered queryset
            return queryset.filter(name__icontains=q)
        # Return the base queryset
        return queryset


class UnionDetail(LoginRequiredMixin, UnionMixin, DetailView):
    
    def get_context_data(self, **kwargs):
        context = super(UnionDetail, self).get_context_data(**kwargs)
        context['members'] = Member.objects.filter(union_id=self.kwargs['pk'])
        return context


class UnionCreate(LoginRequiredMixin, UnionMixin, CreateView):
    form_class = UnionForm
    success_msg = "Union created!"

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
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


class UnionUpdate(LoginRequiredMixin, UnionMixin, UpdateView):
    form_class = UnionForm
    success_msg = "Union updated!"

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(UnionActionMixin, self).form_valid(form)
