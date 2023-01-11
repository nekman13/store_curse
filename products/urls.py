from django.urls import path

from .views import basket_add, basket_delete, IndexView, ProductsListView

app_name = 'products'


urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    path('page/<int:page>', ProductsListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/delete/<int:basket_id>/', basket_delete, name='basket_delete'),

]
