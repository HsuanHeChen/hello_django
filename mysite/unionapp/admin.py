from django.contrib import admin
from .models import Union, Member


# Register your models here.

class MemberInline(admin.TabularInline):
    model = Member
    extra = 1


@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'disabled')
    ordering = ('id',)
    inlines = [MemberInline]
