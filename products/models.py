from django.db import models

from users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='Описание категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(upload_to='products_images', verbose_name='Фото')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name



class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)




class Basket(models.Model):
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество товаров')
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='ПользовательID')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина {self.user}| продукты:{self.product.name}'

    def sum(self):
        sum = self.product.price * self.quantity
        return sum

