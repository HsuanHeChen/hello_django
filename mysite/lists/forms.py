from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['text', ]
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a TODO item.',
                'class': 'form-input',
            }),
        }
        error_messages = {
            'text': {'required': 'You cannot have an empty list item.'}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
