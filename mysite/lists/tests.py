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

    # def test_passes_corrent_list_to_template(self):



class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        new_list = List.objects.create()
        self.client.post('/lists/%d/add_item' % (new_list.id,), data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, new_list)

    def test_redirects_to_list_view(self):
        new_list = List.objects.create()
        response = self.client.post('/lists/%d/add_item' % (new_list.id,), data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        _list = List()
        _list.save()

        first_item = Item()
        first_item.text = 'The first todo.'
        first_item.list = _list
        first_item.save()

        second_item = Item()
        second_item.text = 'The second todo.'
        second_item.list = _list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, _list)

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)
        self.assertEqual(items[0].text, 'The first todo.')
        self.assertEqual(items[0].list, _list)
        self.assertEqual(items[1].text, 'The second todo.')
        self.assertEqual(items[1].list, _list)
