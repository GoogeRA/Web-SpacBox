from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ========================================
# КАТЕГОРИИ И КОМПОНЕНТЫ (существующие)
# ========================================


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # ← Добавьте default

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Component(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='components')
    manufacturer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to='components/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    is_hit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.manufacturer})'


# ========================================
# ПРОФИЛЬ И АККАУНТ (новые)
# ========================================

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email_notifications = models.BooleanField(default=True)
    price_alerts = models.BooleanField(default=True)
    stock_alerts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile: {self.user.username}'


# ========================================
# СБОРКИ (новые)
# ========================================

class SavedBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_builds')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    components = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.user.username})'


# ========================================
# ЗАКАЗЫ (новые)
# ========================================

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.order_number} ({self.user.username})'


# ========================================
# ИЗБРАННОЕ (новые)
# ========================================

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    component = models.ForeignKey('Component', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'component']
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user.username} - {self.component.name}'


# ========================================
# УВЕДОМЛЕНИЯ (новые)
# ========================================

class Notification(models.Model):
    TYPE_CHOICES = [
        ('price', 'Изменение цены'),
        ('stock', 'Появление в наличии'),
        ('order', 'Статус заказа'),
        ('general', 'Общее'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.title}'