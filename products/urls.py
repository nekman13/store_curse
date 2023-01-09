from django.urls import path

from .views import index, products_list, basket_add, basket_delete

app_name = 'products'


urlpatterns = [
    path('', products_list, name='index'),
    path('category/<int:category_id>', products_list, name='category'),
    path('page/<int:page_number>', products_list, name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/delete/<int:basket_id>/', basket_delete, name='basket_delete'),

]
