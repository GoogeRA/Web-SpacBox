from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Component, Category, SavedBuild, Order, Favorite, Notification, UserProfile


@require_POST
def compare_manage(request):
    """AJAX-обработчик для управления списком сравнения"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        component_id = str(data.get('component_id'))
        compare_list = request.session.get('compare', [])

        if action == 'add':
            if len(compare_list) >= 4:
                return JsonResponse({'status': 'error', 'message': 'Максимум 4 компонента для сравнения'}, status=400)
            if component_id not in compare_list:
                compare_list.append(component_id)
        elif action == 'remove':
            if component_id in compare_list:
                compare_list.remove(component_id)
        elif action == 'clear':
            compare_list = []

        request.session['compare'] = compare_list
        request.session.modified = True

        return JsonResponse({
            'status': 'success',
            'count': len(compare_list),
            'in_list': component_id in compare_list
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def compare_view(request):
    """Страница сравнения: собирает компоненты из сессии и формирует строки таблицы"""
    compare_ids = request.session.get('compare', [])
    compare_components = []
    for cid in compare_ids:
        try:
            comp = Component.objects.get(id=cid)
            comp.specs = comp.specifications or {}
            compare_components.append(comp)
        except Component.DoesNotExist:
            continue

    # Собираем все уникальные ключи характеристик
    spec_keys = set()
    for comp in compare_components:
        spec_keys.update(comp.specs.keys())

    # Формируем строки таблицы
    table_rows = [
        {'name': 'Производитель', 'values': [c.manufacturer for c in compare_components]},
        {'name': 'Категория', 'values': [c.category.name if c.category else '—' for c in compare_components]},
        {'name': 'Цена', 'values': [f'{c.price:,.0f} ₽' for c in compare_components]},
    ]

    for key in sorted(spec_keys):
        row_vals = []
        for comp in compare_components:
            val = comp.specs.get(key, '—')
            # Преобразуем списки/словари в строку или ставим прочерк
            row_vals.append(str(val) if not isinstance(val, (list, dict)) else '—')
        table_rows.append({'name': key, 'values': row_vals})

    return render(request, 'core/compare.html', {
        'compare_components': compare_components,
        'table_rows': table_rows
    })

def components(request):
    """... ваш существующий код без изменений ..."""
    # ... (все фильтры, пагинация остаются как есть) ...

    # 👇 ДОБАВЬТЕ эту строку в конец перед return render
    compare_ids = [str(x) for x in request.session.get('compare', [])]

    context = {
        # ... ваши существующие переменные ...
        'compare_ids': compare_ids,  # 👈 ПЕРЕДАЁМ В ШАБЛОН
    }
    return render(request, 'core/components.html', context)

def index(request):
    """Главная страница SpecBox"""
    return render(request, 'core/index.html')


def configurator_view(request):
    """Представление для страницы конфигуратора ПК"""
    return render(request, 'core/configurator.html')


def components(request):
    """Страница комплектующих с фильтрами, поиском и пагинацией"""
    components = Component.objects.select_related('category').all()

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        components = components.filter(
            Q(name__icontains=search_query) | Q(manufacturer__icontains=search_query)
        )

    # Категории
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        components = components.filter(category__name__in=selected_categories)

    # Бренды
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        components = components.filter(manufacturer__in=selected_brands)

    # Цена
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    if price_from:
        components = components.filter(price__gte=price_from)
    if price_to:
        components = components.filter(price__lte=price_to)

    # Сортировка
    sort = request.GET.get('sort', 'popular')
    if sort == 'price_asc':
        components = components.order_by('price')
    elif sort == 'price_desc':
        components = components.order_by('-price')
    else:
        components = components.order_by('name')

    # Пагинация
    paginator = Paginator(components, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Фильтры для сайдбара
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
    logout(request)
    return redirect('core:index')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        terms = request.POST.get('terms')

        if password != password_confirm:
            return render(request, 'registration/register.html',
                          {'error': 'Пароли не совпадают', 'username': username, 'email': email})
        if len(password) < 8:
            return render(request, 'registration/register.html',
                          {'error': 'Пароль минимум 8 символов', 'username': username, 'email': email})
        if not terms:
            return render(request, 'registration/register.html',
                          {'error': 'Примите условия использования', 'username': username, 'email': email})
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html',
                          {'error': 'Пользователь уже существует', 'username': username, 'email': email})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('core:profile')
    return render(request, 'registration/register.html')


@login_required(login_url='core:login')
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    user_data = {
        'username': user.username,
        'email': user.email,
        'phone': profile.phone or 'Не указан',
        'city': profile.city or 'Не указан',
        'registered': user.date_joined.strftime('%d.%m.%Y'),
        'last_login': user.last_login.strftime('%d.%m.%Y %H:%M') if user.last_login else 'Неизвестно',
    }

    saved_builds = SavedBuild.objects.filter(user=user)[:5]
    saved_builds_data = [
        {
            'id': build.id, 'name': build.name,
            'created_at': build.created_at.strftime('%d.%m.%Y'),
            'cpu': build.components.get('cpu', 'Не указано'),
            'gpu': build.components.get('gpu', 'Не указано'),
            'ram': build.components.get('ram', 'Не указано'),
            'total_price': build.total_price,
        } for build in saved_builds
    ]

    orders = Order.objects.filter(user=user)[:5]
    orders_data = [
        {
            'id': order.order_number, 'created_at': order.created_at.strftime('%d.%m.%Y'),
            'status': order.status, 'status_display': order.get_status_display(),
            'total': order.total_price,
        } for order in orders
    ]

    favorites = Favorite.objects.filter(user=user).select_related('component')[:5]
    favorites_data = [
        {
            'id': fav.id,
            'component': {
                'name': fav.component.name,
                'category': fav.component.category.name if fav.component.category else 'Без категории',
                'manufacturer': fav.component.manufacturer,
                'price': fav.component.price,
                'in_stock': fav.component.in_stock,
            }
        } for fav in favorites
    ]

    notifications = Notification.objects.filter(user=user, is_read=False)[:10]
    notifications_data = [
        {
            'id': notif.id, 'message': notif.message,
            'type': notif.notification_type,
            'created_at': get_time_ago(notif.created_at),
            'is_read': notif.is_read,
        } for notif in notifications
    ]

    context = {
        'user_data': user_data,
        'saved_builds': saved_builds_data,
        'saved_builds_count': SavedBuild.objects.filter(user=user).count(),
        'orders': orders_data,
        'orders_count': Order.objects.filter(user=user).count(),
        'favorites': favorites_data,
        'favorites_count': Favorite.objects.filter(user=user).count(),
        'notifications': notifications_data,
        'unread_notifications': Notification.objects.filter(user=user, is_read=False).count(),
    }
    return render(request, 'core/profile.html', context)


def component_detail_view(request, component_id):
    """Страница детального просмотра компонента"""
    component = get_object_or_404(Component, id=component_id)

    # ✅ Добавляем псевдоним specs, чтобы ваш шаблон {{ component.specs }} работал без изменений
    component.specs = component.specifications or {}

    return render(request, 'core/component_detail.html', {'component': component})

def cart_view(request):
    return render(request, 'core/cart.html')

def get_time_ago(dt):
    """Возвращает время в формате '2 часа назад'"""
    now = timezone.now()
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return 'Только что'
    elif seconds < 3600:
        return f'{int(seconds // 60)} мин. назад'
    elif seconds < 86400:
        return f'{int(seconds // 3600)} час. назад'
    elif seconds < 604800:
        return f'{int(seconds // 86400)} дн. назад'
    else:
        return dt.strftime('%d.%m.%Y')

@require_POST
def add_to_cart(request):
    """Добавляет компонент в корзину (сессия Django)"""
    try:
        data = json.loads(request.body)
        component_id = str(data.get('component_id'))
        if not component_id:
            return JsonResponse({'status': 'error', 'message': 'ID не указан'}, status=400)

        cart = request.session.get('cart', {})
        cart[component_id] = cart.get(component_id, 0) + 1
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'status': 'success',
            'total_items': sum(cart.values()),
            'message': 'Товар добавлен в корзину'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def remove_from_cart(request):
    """Удаляет компонент из корзины"""
    data = json.loads(request.body)
    component_id = str(data.get('component_id'))
    cart = request.session.get('cart', {})
    cart.pop(component_id, None)
    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'status': 'success', 'total_items': sum(cart.values())})

@require_POST
def update_cart_quantity(request):
    """Обновляет количество товара в корзине"""
    data = json.loads(request.body)
    component_id = str(data.get('component_id'))
    quantity = int(data.get('quantity', 1))
    if quantity < 1:
        return remove_from_cart(request)
    cart = request.session.get('cart', {})
    cart[component_id] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'status': 'success', 'total_items': sum(cart.values())})

def cart_view(request):
    """Страница корзины"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_count = 0

    for comp_id, qty in cart.items():
        try:
            comp = Component.objects.get(id=comp_id)
            line_total = comp.price * qty
            cart_items.append({
                'component': comp,
                'quantity': qty,
                'line_total': line_total
            })
            total_price += line_total
            total_count += qty
        except Component.DoesNotExist:
            pass

    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_count': total_count
    })