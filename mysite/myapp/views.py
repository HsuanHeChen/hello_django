from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import Product
from .form import ProductForm

# Create your views here.


# def hello_world(request, name=""):
#     current_time = datetime.now()
#     return render(request, 'hello_world.html', locals())
class HelloWord(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'hello_world.html', {'current_time': datetime.now()})


def products(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'products.html', locals())


def product_detail(request, id):
    product = Product.objects.get(id=id)
    product.press += 1
    product.save()

    return render(request, 'product_detail.html', locals())


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return HttpResponseRedirect('/products/' + str(product.id))

    form = ProductForm()
    return render(request, 'product_create.html', locals())


def product_edit(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.sku = request.POST['sku']
        product.photo = request.POST['photo']
        product.save()
        return HttpResponseRedirect('/products/' + str(product.id))

    form = ProductForm({'name': product.name, 'sku': product.sku, 'photo': product.photo })
    return render(request, 'product_edit.html', locals())


def product_delete(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
    except:
        message = "error!"

    return HttpResponseRedirect('/products')
