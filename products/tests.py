from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTests(TestCase):
    def test_view(self):
        path = reverse("index")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["title"], "Store - главная страница")


class ProductListViewTests(TestCase):

    fixtures = ["products.json", "categories.json"]

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse("products:index")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["title"], "Store - каталог")
        self.assertEqual(
            list(response.context_data["products"]), list(self.products[:3])
        )
        self.assertTemplateUsed(response, "products/products.html")

    def test_list_category(self):
        path = reverse("products:index")
        category = ProductCategory.objects.first()
        response = self.client.get(path, {"category_id": category.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["title"], "Store - каталог")
        self.assertTemplateUsed(response, "products/products.html")
