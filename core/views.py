from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from core.models import Component, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    """Главная страница SpecBox"""
    return render(request, 'core/index.html')


def configurator_view(request):
    """Представление для страницы конфигуратора ПК"""
    return render(request, 'core/configurator.html')


def components(request):
    """Страница комплектующих с фильтрами, поиском и пагинацией"""
    # Базовый queryset
    components = Component.objects.select_related('category').all()

    # === ПОИСК ===
    search_query = request.GET.get('search', '')
    if search_query:
        components = components.filter(
            Q(name__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )

    # === КАТЕГОРИИ ===
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        components = components.filter(category__name__in=selected_categories)

    # === БРЕНДЫ ===
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        components = components.filter(manufacturer__in=selected_brands)

    # === ЦЕНА ===
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    if price_from:
        components = components.filter(price__gte=price_from)
    if price_to:
        components = components.filter(price__lte=price_to)

    # === СОРТИРОВКА ===
    sort = request.GET.get('sort', 'popular')
    if sort == 'price_asc':
        components = components.order_by('price')
    elif sort == 'price_desc':
        components = components.order_by('-price')
    else:
        components = components.order_by('name')

    # === ПАГИНАЦИЯ ===
    paginator = Paginator(components, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # === Категории и бренды для фильтров ===
    categories = Category.objects.all().order_by('name').distinct()
    brands = Component.objects.values_list('manufacturer', flat=True).distinct().order_by('manufacturer')

    context = {
        'components': page_obj,
        'total_count': paginator.count,
        'categories': categories,
        'brands': brands,
        'selected_categories': selected_categories,
        'selected_brands': selected_brands,
        'sort': sort,
        'page_obj': page_obj,
        'paginator': paginator,
    }

    return render(request, 'core/components.html', context)


def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:profile')
        else:
            return render(request, 'registration/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'registration/login.html')

def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('core:index')

def register_view(request):
    """Страница регистрации"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        terms = request.POST.get('terms')

        if password != password_confirm:
            return render(request, 'registration/register.html', {
                'error': 'Пароли не совпадают',
                'username': username,
                'email': email,
            })

        if len(password) < 8:
            return render(request, 'registration/register.html', {
                'error': 'Пароль должен быть минимум 8 символов',
                'username': username,
                'email': email,
            })

        if not terms:
            return render(request, 'registration/register.html', {
                'error': 'Необходимо согласиться с условиями использования',
                'username': username,
                'email': email,
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {
                'error': 'Пользователь с таким именем уже существует',
                'username': username,
                'email': email,
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)

        return redirect('core:profile')

    return render(request, 'registration/register.html')


@login_required(login_url='core:login')
def profile_view(request):
    """Личный кабинет пользователя"""

    # Данные сохраненных сборок (заглушка)
    saved_builds = [
        {
            'id': 1,
            'name': 'Игровой ПК 2026',
            'created_at': '28.01.2026',
            'cpu': 'AMD Ryzen 9 7950X',
            'gpu': 'NVIDIA GeForce RTX 4090',
            'ram': '32GB DDR5',
            'total_price': 350000,
        },
    ]

    # Данные заказов (заглушка)
    orders = [
        {
            'id': 1001,
            'created_at': '27.01.2026',
            'status': 'completed',
            'status_display': 'Выполнен',
            'total': 350000,
        },
    ]

    # Избранные товары (заглушка)
    favorites = [
        {
            'id': 1,
            'component': {
                'name': 'NVIDIA GeForce RTX 4090',
                'category': 'Видеокарты',
                'manufacturer': 'NVIDIA',
                'price': 189990,
                'in_stock': True,
            }
        },
    ]

    # Уведомления (заглушка)
    notifications = [
        {
            'id': 1,
            'message': 'Цена на NVIDIA GeForce RTX 4090 снизилась на 5%',
            'type': 'price',
            'created_at': '2 часа назад',
            'is_read': False,
        },
    ]

    # Данные пользователя
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        'phone': '+7 (999) 123-45-67',
        'city': 'Москва',
        'registered': '15.12.2025',
        'last_login': request.user.last_login.strftime('%d.%m.%Y %H:%M') if request.user.last_login else 'Неизвестно',
    }

    context = {
        'user_data': user_data,
        'saved_builds': saved_builds,
        'saved_builds_count': len(saved_builds),
        'orders': orders,
        'orders_count': len(orders),
        'favorites': favorites,
        'favorites_count': len(favorites),
        'notifications': notifications,
        'unread_notifications': len([n for n in notifications if not n['is_read']]),
    }

    return render(request, 'core/profile.html', context)