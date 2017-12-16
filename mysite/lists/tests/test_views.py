from django.test import TestCase
from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ItemForm, ExistingListItemForm

# Create your tests here.


class ListPageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/lists/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_use_item_form(self):
        response = self.client.get('/lists/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        _list = List.objects.create()
        response = self.client.get('/lists/%d/' % (_list.id,))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_only_items_for_the_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='correct item1', list=correct_list)
        Item.objects.create(text='correct item2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other item1", list=other_list)
        Item.objects.create(text="other item2", list=other_list)

        response = self.client.get("/lists/%d/" % (correct_list.id,))
        self.assertContains(response, 'correct item1')
        self.assertContains(response, 'correct item2')
        self.assertNotContains(response, "other item1")
        self.assertNotContains(response, "other item2")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        new_list = List.objects.create()
        self.client.post('/lists/%d/' % (new_list.id,), data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, new_list)

    def test_redirects_to_list_view(self):
        new_list = List.objects.create()
        response = self.client.post('/lists/%d/' % (new_list.id,), data={'text': 'A new list item'})
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def post_invalid_input(self):
        _list = List.objects.create()
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
        _list = List.objects.create()
        response = self.client.get('/lists/%d/' % (_list.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplication_item_validation_errors_end_up_on_list_page(self):
        _list = List.objects.create()
        Item.objects.create(text='ft_item', list=_list)
        response = self.client.post('/lists/%d/' % (_list.id,), data={'text': 'ft_item'})
        self.assertContains(response, DUPLICATE_ITEM_ERROR)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


class NewListTest(TestCase):

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
