from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Component, Category, SavedBuild, Order, Favorite, Notification, UserProfile


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