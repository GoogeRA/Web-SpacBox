from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    """Главная страница SpecBox"""
    return render(request, 'core/index.html')


def configurator_view(request):
    """Представление для страницы конфигуратора ПК"""
    return render(request, 'core/configurator.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:profile')  # Перенаправление в ЛК
        else:
            return render(request, 'registration/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'registration/login.html')


def register_view(request):
    """Страница регистрации"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            return render(request, 'core/register.html', {'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Пользователь уже существует'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('core:profile')

    return render(request, 'core/register.html')

def components(request):
    """Страница комплектующих"""
    components_list = [
        {
            'id': 1,
            'name': 'NVIDIA GeForce RTX 4090',
            'category': 'Видеокарты',
            'price': 189990,
            'manufacturer': 'NVIDIA',
            'in_stock': True,
            'is_hit': True,
        },
        {
            'id': 2,
            'name': 'AMD Ryzen 9 7950X',
            'category': 'Процессоры',
            'price': 54990,
            'manufacturer': 'AMD',
            'in_stock': True,
            'is_hit': True,
        },
        {
            'id': 3,
            'name': 'Intel Core i9-14900K',
            'category': 'Процессоры',
            'price': 59990,
            'manufacturer': 'Intel',
            'in_stock': True,
            'is_hit': False,
        },
        {
            'id': 4,
            'name': 'Kingston Fury 32GB DDR5',
            'category': 'Оперативная память',
            'price': 14990,
            'manufacturer': 'Kingston',
            'in_stock': True,
            'is_hit': False,
        },
        {
            'id': 5,
            'name': 'Samsung 990 PRO 2TB',
            'category': 'SSD накопители',
            'price': 19990,
            'manufacturer': 'Samsung',
            'in_stock': True,
            'is_hit': True,
        },
        {
            'id': 6,
            'name': 'ASUS ROG MAXIMUS Z790',
            'category': 'Материнские платы',
            'price': 64990,
            'manufacturer': 'ASUS',
            'in_stock': False,
            'is_hit': False,
        },
        {
            'id': 7,
            'name': 'NZXT Kraken Elite 360',
            'category': 'Охлаждение',
            'price': 24990,
            'manufacturer': 'NZXT',
            'in_stock': True,
            'is_hit': False,
        },
        {
            'id': 8,
            'name': 'Seasonic PRIME TX-1000',
            'category': 'Блоки питания',
            'price': 29990,
            'manufacturer': 'Seasonic',
            'in_stock': True,
            'is_hit': False,
        },
    ]

    context = {
        'components': components_list,
        'total_count': len(components_list),
    }

    return render(request, 'core/components.html', context)


def profile_view(request):
    """
    Личный кабинет пользователя (без авторизации)
    Демо-данные для тестирования интерфейса
    """
    # Демо-данные сборок
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
        {
            'id': 2,
            'name': 'Рабочая станция',
            'created_at': '25.01.2026',
            'cpu': 'Intel Core i9-14900K',
            'gpu': 'NVIDIA GeForce RTX 4070',
            'ram': '64GB DDR5',
            'total_price': 280000,
        },
        {
            'id': 3,
            'name': 'Бюджетный гейминг',
            'created_at': '20.01.2026',
            'cpu': 'AMD Ryzen 5 7600X',
            'gpu': 'NVIDIA GeForce RTX 4060',
            'ram': '16GB DDR5',
            'total_price': 120000,
        },
    ]

    # Демо-данные заказов
    orders = [
        {
            'id': 1001,
            'created_at': '27.01.2026',
            'status': 'completed',
            'status_display': 'Выполнен',
            'total': 350000,
        },
        {
            'id': 1002,
            'created_at': '28.01.2026',
            'status': 'processing',
            'status_display': 'В обработке',
            'total': 125000,
        },
        {
            'id': 1003,
            'created_at': '26.01.2026',
            'status': 'shipped',
            'status_display': 'Отправлен',
            'total': 89000,
        },
    ]

    # Демо-данные избранного
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
        {
            'id': 2,
            'component': {
                'name': 'AMD Ryzen 9 7950X',
                'category': 'Процессоры',
                'manufacturer': 'AMD',
                'price': 54990,
                'in_stock': True,
            }
        },
        {
            'id': 3,
            'component': {
                'name': 'Samsung 990 PRO 2TB',
                'category': 'SSD накопители',
                'manufacturer': 'Samsung',
                'price': 19990,
                'in_stock': True,
            }
        },
    ]

    # Демо-данные уведомлений
    notifications = [
        {
            'id': 1,
            'message': 'Цена на NVIDIA GeForce RTX 4090 снизилась на 5%',
            'type': 'price',
            'created_at': '2 часа назад',
            'is_read': False,
        },
        {
            'id': 2,
            'message': 'Компонент ASUS ROG MAXIMUS Z790 появился в наличии',
            'type': 'stock',
            'created_at': '5 часов назад',
            'is_read': True,
        },
        {
            'id': 3,
            'message': 'Ваш заказ #1001 готов к выдаче',
            'type': 'order',
            'created_at': '1 день назад',
            'is_read': True,
        },
    ]

    # Демо-данные пользователя
    user_data = {
        'username': 'Gamer2026',
        'email': 'gamer@example.com',
        'phone': '+7 (999) 123-45-67',
        'city': 'Москва',
        'registered': '15.12.2025',
        'last_login': '28.01.2026 14:30',
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