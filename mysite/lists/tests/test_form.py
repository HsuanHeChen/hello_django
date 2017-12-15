from django.test import TestCase
from lists.forms import ItemForm
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a TODO item."', form.as_p())
        self.assertIn('class="form-input"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ["You cannot have an empty list item."])

    def test_form_save_handles_saving_to_a_list(self):
        form = ItemForm(data={'text': 'do me'})
        _list = List.objects.create()
        new_item = form.save(for_list=_list)
        self.assertEqual(new_item, Item.objects.last())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, _list)
