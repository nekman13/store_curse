from django.db import models



class ProductCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='Описание категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(upload_to='products_images', verbose_name='Фото')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')


    def __str__(self):
        return self.name

