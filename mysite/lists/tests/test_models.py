from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ListItemModelsTest(TestCase):

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

    def test_cant_save_empty_list_items(self):
        _list = List.objects.create()
        item = Item(list=_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        _list = List.objects.create()
        self.assertEqual(_list.get_absolute_url(), '/lists/%d/' % (_list.id,))
