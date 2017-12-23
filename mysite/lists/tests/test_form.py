import unittest
from unittest.mock import Mock, patch
from lists.models import List, Item
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ItemForm, ExistingListItemForm, NewListForm
from .base import ListsTestCase


class ItemFormTest(ListsTestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a TODO item."', form.as_p())
        self.assertIn('class="form-input"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


class ExistingListItemFormTest(ListsTestCase):

    def test_form_renders_item_text_input(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        form = ExistingListItemForm(for_list=_list)
        self.assertIn('placeholder="Enter a TODO item."', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        Item.objects.create(list=_list, text='no twins!')
        form = ExistingListItemForm(for_list=_list, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        form = ExistingListItemForm(for_list=_list, data={'text': 'item'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.last())


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(self, mock_list_create_new):
        user = Mock(is_authenticated=lambda: False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(first_item_text='new item text')

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_authenticated(self, mock_list_create_new):
        user = Mock(is_authenticated=lambda: True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(first_item_text='new item text', owner=user)

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_list_create_new):
        user = Mock(is_authenticated=lambda: True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_list_create_new.return_value)
