from django.shortcuts import render

from .models import Product, ProductCategory


# Create your views here.

def index(request):
   return render(request, 'products/index.html')


# todo контроллер вывода всех продуктов
def products(request):
   context = {
      'products': Product.objects.all(),
      'categories': ProductCategory.objects.all(),
   }
   return render(request, 'products/products.html', context=context)