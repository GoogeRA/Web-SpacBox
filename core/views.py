from django.shortcuts import render


def index(request):
    """Главная страница SpecBox"""
    return render(request, 'core/index.html')


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