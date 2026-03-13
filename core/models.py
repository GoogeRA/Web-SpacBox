from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Component(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    manufacturer = models.CharField(max_length=100, verbose_name='Производитель')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    is_hit = models.BooleanField(default=False, verbose_name='Хит')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
        ordering = ['name']

    def __str__(self):
        return self.name

    