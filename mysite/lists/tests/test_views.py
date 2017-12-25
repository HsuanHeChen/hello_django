import unittest
from unittest.mock import Mock, patch
from django.http import HttpRequest
from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ItemForm, ExistingListItemForm
from lists.views import new_list
from .base import ListsTestCase


class ListPageTest(ListsTestCase):

    def test_uses_home_template(self):
        response = self.client.get('/lists/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_use_item_form(self):
        response = self.client.get('/lists/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(ListsTestCase):

    def test_uses_list_template(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        response = self.client.get('/lists/%d/' % (_list.id,))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_only_items_for_the_list(self):
        owner = self.init_owner()
        correct_list = List.objects.create(owner=owner)
        Item.objects.create(text='correct item1', list=correct_list)
        Item.objects.create(text='correct item2', list=correct_list)
        other_list = List.objects.create(owner=owner)
        Item.objects.create(text="other item1", list=other_list)
        Item.objects.create(text="other item2", list=other_list)

        response = self.client.get("/lists/%d/" % (correct_list.id,))
        self.assertContains(response, 'correct item1')
        self.assertContains(response, 'correct item2')
        self.assertNotContains(response, "other item1")
        self.assertNotContains(response, "other item2")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        owner = self.init_owner()
        new_list = List.objects.create(owner=owner)
        self.client.post('/lists/%d/' % (new_list.id,), data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, new_list)

    def test_redirects_to_list_view(self):
        owner = self.init_owner()
        new_list = List.objects.create(owner=owner)
        response = self.client.post('/lists/%d/' % (new_list.id,), data={'text': 'A new list item'})
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def post_invalid_input(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        return self.client.post('/lists/%d/' % (_list.id,), data={'text': ''})

    def test_for_invalid_input_no_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_render_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_pass_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_show_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_display_item_form(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        response = self.client.get('/lists/%d/' % (_list.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplication_item_validation_errors_end_up_on_list_page(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        Item.objects.create(text='ft_item', list=_list)
        response = self.client.post('/lists/%d/' % (_list.id,), data={'text': 'ft_item'})
        self.assertContains(response, DUPLICATE_ITEM_ERROR)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


class NewListViewIntegratedTest(ListsTestCase):

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_error_are_show_on_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = self.init_owner()
        request.POST['text'] = 'aaa list'
        # new_list中如果不是使用List() 這邊會噴錯
        new_list(request)
        _list = List.objects.first()
        self.assertEqual(_list.owner, request.user)


class MyListsTest(ListsTestCase):

    def test_my_lists_url_render_my_lists_template(self):
        owner = self.init_owner()
        response = self.client.get('/lists/users/{}/'.format(owner.id))
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_pass_correct_owner_to_template(self):
        owner = self.init_owner()
        response = self.client.get('/lists/users/{}/'.format(owner.id))
        self.assertEqual(response.context['owner'], owner)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'aaa list'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_from_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_render_home_template_with_form_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'lists/home.html', {'form': mock_form})

    @patch('lists.views.render')
    def test_does_not_save_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)
