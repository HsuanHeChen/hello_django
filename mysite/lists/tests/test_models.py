from django.core.exceptions import ValidationError
from lists.models import Item, List
from .base import ListsTestCase


class ListModelsTest(ListsTestCase):

    def test_get_absolute_url(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        self.assertEqual(_list.get_absolute_url(), '/lists/%d/' % (_list.id,))

    def test_list_can_have_owner(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        self.assertIn(_list, owner.list_set.all())

    def test_list_name_is_first_item_text(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        Item.objects.create(list=_list, text='item1')
        Item.objects.create(list=_list, text='item2')
        self.assertEqual(_list.name, 'item1')

    def test_create_new_creates_lists_and_first_item(self):
        List.create_new(first_item_text='item1')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'item1')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        owner = self.init_owner()
        List.create_new(first_item_text='item1', owner=owner)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, owner)

    def test_lists_can_have_owners(self):
        owner = self.init_owner()
        List(owner=owner)

    def test_list_owner_is_optional(self):
        List().full_clean()

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text='item1')
        new_list = List.objects.first()
        self.assertEqual(new_list, returned)


class ItemModelsTest(ListsTestCase):

    def test_defafult_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        item = Item()
        item.list = _list
        item.save()
        self.assertIn(item, _list.item_set.all())

    def test_list_ordering(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        item1 = Item.objects.create(list=_list, text='item1')
        item2 = Item.objects.create(list=_list, text='item2')
        item3 = Item.objects.create(list=_list, text='item3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_cant_save_empty_list_items(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        item = Item(list=_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        owner = self.init_owner()
        _list = List.objects.create(owner=owner)
        Item.objects.create(list=_list, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=_list, text='bla')
            item.full_clean()

    def test_can_save_same_item_in_different_lists(self):
        owner = self.init_owner()
        list1 = List.objects.create(owner=owner)
        list2 = List.objects.create(owner=owner)
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # 應該要過
