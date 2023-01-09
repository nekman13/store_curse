from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Product, ProductCategory, Basket


# Create your views here.

def index(request):
   return render(request, 'products/index.html')


# todo контроллер вывода всех продуктов
def products_list(request, category_id=None, page_number=1):
   if category_id:
      products = Product.objects.filter(category__id=category_id)
   else:
      products = Product.objects.all()

   per_page = 3
   paginator = Paginator(products, per_page)
   products_paginator = paginator.page(page_number)
   context = {
      'products': products_paginator,
      'categories': ProductCategory.objects.all(),
   }
   return render(request, 'products/products.html', context=context)

@login_required()
def basket_add(request, product_id):
   product = Product.objects.get(id=product_id)
   baskets = Basket.objects.filter(user=request.user, product=product)

   if not baskets.exists():
      Basket.objects.create(user=request.user, product=product, quantity=1)
   else:
      basket = baskets.first()
      basket.quantity += 1
      basket.save()

   return redirect(request.META['HTTP_REFERER'])
@login_required()
def basket_delete(request, basket_id):
   basket = Basket.objects.get(id=basket_id)
   basket.delete()

   return redirect(reverse_lazy('users:profile'))
