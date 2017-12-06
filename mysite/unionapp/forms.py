from django import forms
from . import models


class UnionForm(forms.ModelForm):
    class Meta:
        model = models.Union
        fields = ['name']
        # HELP: NOT WORK in create/update.
        # fields = ['name', 'photo']
