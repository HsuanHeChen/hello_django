from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ListModelsTest(TestCase):

    def test_get_absolute_url(self):
        _list = List.objects.create()
        self.assertEqual(_list.get_absolute_url(), '/lists/%d/' % (_list.id,))


class ItemModelsTest(TestCase):

    def test_defafult_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        _list = List.objects.create()
        item = Item()
        item.list = _list
        item.save()
        self.assertIn(item, _list.item_set.all())

    def test_list_ordering(self):
        _list = List.objects.create()
        item1 = Item.objects.create(list=_list, text='item1')
        item2 = Item.objects.create(list=_list, text='item2')
        item3 = Item.objects.create(list=_list, text='item3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_cant_save_empty_list_items(self):
        _list = List.objects.create()
        item = Item(list=_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        _list = List.objects.create()
        Item.objects.create(list=_list, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=_list, text='bla')
            item.full_clean()

    def test_can_save_same_item_in_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # 應該要過
