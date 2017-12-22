from django import forms
from django.core.exceptions import ValidationError
from .models import Item, List

EMPTY_ITEM_ERROR = "You cannot have an empty list item."
DUPLICATE_ITEM_ERROR = "You have already got this."


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
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated():
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])
