from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView

from .models import Product, ProductCategory, Basket


# Create your views here.

class IndexView(TemplateView):
   template_name = 'products/index.html'
   def get_context_data(self, **kwargs):
      context = super(IndexView, self).get_context_data(**kwargs)
      context['title'] = 'Store'

      return context


# todo контроллер вывода всех продуктов
class ProductsListView(ListView):

   model = Product
   context_object_name = 'products'
   template_name = 'products/products.html'
   paginate_by = 3

   def get_context_data(self, *, object_list=None, **kwargs):
      context = super(ProductsListView, self).get_context_data(**kwargs)
      context['categories'] = ProductCategory.objects.all()
      return context

   def get_queryset(self):
      queryset = super(ProductsListView, self).get_queryset()
      category_id = self.kwargs.get('category_id')
      return queryset.filter(category_id=category_id) if category_id else queryset



#

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




# def products_list(request, category_id=None, page_number=1):
#    if category_id:
#       products = Product.objects.filter(category__id=category_id)
#    else:
#       products = Product.objects.all()
#
#    per_page = 3
#    paginator = Paginator(products, per_page)
#    products_paginator = paginator.page(page_number)
#    context = {
#       'products': products_paginator,
#       'categories': ProductCategory.objects.all(),
#    }
#    return render(request, 'products/products.html', context=context)