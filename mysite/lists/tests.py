from django.test import TestCase
from lists.models import Item

# Create your tests here.


class ListPageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/lists/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_display_all_list_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/')
        self.assertIn('item1', response.content.decode())
        self.assertIn('item2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first todo.'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second todo.'
        second_item.save()

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)
        self.assertEqual(items[0].text, 'The first todo.')
        self.assertEqual(items[1].text, 'The second todo.')
