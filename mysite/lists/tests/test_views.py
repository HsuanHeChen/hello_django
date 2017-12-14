from django.test import TestCase
from lists.models import Item, List

# Create your tests here.


class ListPageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/lists/')
        self.assertTemplateUsed(response, 'lists/home.html')


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
        self.client.post('/lists/%d/' % (new_list.id,), data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, new_list)

    def test_redirects_to_list_view(self):
        new_list = List.objects.create()
        response = self.client.post('/lists/%d/' % (new_list.id,), data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_end_up_on_list_page(self):
        _list = List.objects.create()
        response = self.client.post('/lists/%d/' % (_list.id,), data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertContains(response, 'You cannot have an empty list item.')


class NewListTest(TestCase):

    def test_validation_errors_are_send_back_to_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        self.assertContains(response, 'You cannot have an empty list item.')

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
