from django.test import TestCase
from lists.models import List, Item
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ItemForm, ExistingListItemForm


class ItemFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a TODO item."', form.as_p())
        self.assertIn('class="form-input"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        form = ItemForm(data={'text': 'do me'})
        _list = List.objects.create()
        new_item = form.save(for_list=_list)
        self.assertEqual(new_item, Item.objects.last())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, _list)


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        _list = List.objects.create()
        form = ExistingListItemForm(for_list=_list)
        self.assertIn('placeholder="Enter a TODO item."', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        _list = List.objects.create()
        Item.objects.create(list=_list, text='no twins!')
        form = ExistingListItemForm(for_list=_list, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        _list = List.objects.create()
        form = ExistingListItemForm(for_list=_list, data={'text': 'item'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.last())
