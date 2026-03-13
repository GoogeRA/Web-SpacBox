from django.core.management.base import BaseCommand
from core.models import Category, Component
from decimal import Decimal


class Command(BaseCommand):
    help = 'Наполняет базу данных 100 компонентами для сборки ПК'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Начинаю наполнение базы данных...'))

        # === 1. Создаём категории ===
        categories_data = [
            {'name': 'Процессоры', 'slug': 'processory'},
            {'name': 'Видеокарты', 'slug': 'videokarty'},
            {'name': 'Материнские платы', 'slug': 'materinskie-platy'},
            {'name': 'Оперативная память', 'slug': 'operativnaya-pamyat'},
            {'name': 'SSD накопители', 'slug': 'ssd-nakopiteli'},
            {'name': 'Блоки питания', 'slug': 'bloki-pitaniya'},
            {'name': 'Охлаждение', 'slug': 'ohlazhdenie'},
            {'name': 'Корпуса', 'slug': 'korpusa'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['name']] = cat
            status = '✅ Создана' if created else '⚠️ Уже существует'
            self.stdout.write(f'Категория: {cat_data["name"]} — {status}')

        # === 2. Компоненты (100 штук) ===
        components_data = [
            # ===== ПРОЦЕССОРЫ (15 шт) =====
            # AMD
            {'name': 'AMD Ryzen 9 7950X', 'category': 'Процессоры', 'price': 54990, 'manufacturer': 'AMD',
             'is_hit': True},
            {'name': 'AMD Ryzen 9 7950X3D', 'category': 'Процессоры', 'price': 64990, 'manufacturer': 'AMD',
             'is_hit': True},
            {'name': 'AMD Ryzen 9 7900X', 'category': 'Процессоры', 'price': 44990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Ryzen 7 7700X', 'category': 'Процессоры', 'price': 34990, 'manufacturer': 'AMD',
             'is_hit': True},
            {'name': 'AMD Ryzen 7 7800X3D', 'category': 'Процессоры', 'price': 39990, 'manufacturer': 'AMD',
             'is_hit': True},
            {'name': 'AMD Ryzen 5 7600X', 'category': 'Процессоры', 'price': 24990, 'manufacturer': 'AMD',
             'is_hit': True},
            {'name': 'AMD Ryzen 5 7500F', 'category': 'Процессоры', 'price': 16990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Ryzen 7 5700X', 'category': 'Процессоры', 'price': 19990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Ryzen 5 5600', 'category': 'Процессоры', 'price': 12990, 'manufacturer': 'AMD',
             'is_hit': True},
            # Intel
            {'name': 'Intel Core i9-14900K', 'category': 'Процессоры', 'price': 59990, 'manufacturer': 'Intel',
             'is_hit': True},
            {'name': 'Intel Core i9-14900KF', 'category': 'Процессоры', 'price': 54990, 'manufacturer': 'Intel',
             'is_hit': False},
            {'name': 'Intel Core i7-14700K', 'category': 'Процессоры', 'price': 44990, 'manufacturer': 'Intel',
             'is_hit': True},
            {'name': 'Intel Core i7-14700KF', 'category': 'Процессоры', 'price': 39990, 'manufacturer': 'Intel',
             'is_hit': False},
            {'name': 'Intel Core i5-14600K', 'category': 'Процессоры', 'price': 32990, 'manufacturer': 'Intel',
             'is_hit': True},
            {'name': 'Intel Core i5-14400F', 'category': 'Процессоры', 'price': 19990, 'manufacturer': 'Intel',
             'is_hit': False},

            # ===== ВИДЕОКАРТЫ (20 шт) =====
            # NVIDIA RTX 40xx
            {'name': 'NVIDIA GeForce RTX 4090 24GB', 'category': 'Видеокарты', 'price': 189990,
             'manufacturer': 'NVIDIA', 'is_hit': True},
            {'name': 'NVIDIA GeForce RTX 4080 SUPER 16GB', 'category': 'Видеокарты', 'price': 129990,
             'manufacturer': 'NVIDIA', 'is_hit': True},
            {'name': 'NVIDIA GeForce RTX 4080 16GB', 'category': 'Видеокарты', 'price': 119990,
             'manufacturer': 'NVIDIA', 'is_hit': False},
            {'name': 'NVIDIA GeForce RTX 4070 Ti SUPER 16GB', 'category': 'Видеокарты', 'price': 99990,
             'manufacturer': 'NVIDIA', 'is_hit': True},
            {'name': 'NVIDIA GeForce RTX 4070 Ti 12GB', 'category': 'Видеокарты', 'price': 89990,
             'manufacturer': 'NVIDIA', 'is_hit': False},
            {'name': 'NVIDIA GeForce RTX 4070 SUPER 12GB', 'category': 'Видеокарты', 'price': 79990,
             'manufacturer': 'NVIDIA', 'is_hit': True},
            {'name': 'NVIDIA GeForce RTX 4070 12GB', 'category': 'Видеокарты', 'price': 69990, 'manufacturer': 'NVIDIA',
             'is_hit': False},
            {'name': 'NVIDIA GeForce RTX 4060 Ti 16GB', 'category': 'Видеокарты', 'price': 54990,
             'manufacturer': 'NVIDIA', 'is_hit': False},
            {'name': 'NVIDIA GeForce RTX 4060 Ti 8GB', 'category': 'Видеокарты', 'price': 44990,
             'manufacturer': 'NVIDIA', 'is_hit': True},
            {'name': 'NVIDIA GeForce RTX 4060 8GB', 'category': 'Видеокарты', 'price': 34990, 'manufacturer': 'NVIDIA',
             'is_hit': True},
            # AMD Radeon
            {'name': 'AMD Radeon RX 7900 XTX 24GB', 'category': 'Видеокарты', 'price': 109990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Radeon RX 7900 XT 20GB', 'category': 'Видеокарты', 'price': 89990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Radeon RX 7800 XT 16GB', 'category': 'Видеокарты', 'price': 64990, 'manufacturer': 'AMD',
             'is_hit': True},
            {'name': 'AMD Radeon RX 7700 XT 12GB', 'category': 'Видеокарты', 'price': 49990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Radeon RX 7600 8GB', 'category': 'Видеокарты', 'price': 34990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Radeon RX 6750 XT 12GB', 'category': 'Видеокарты', 'price': 39990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Radeon RX 6650 XT 8GB', 'category': 'Видеокарты', 'price': 29990, 'manufacturer': 'AMD',
             'is_hit': False},
            {'name': 'AMD Radeon RX 6600 8GB', 'category': 'Видеокарты', 'price': 24990, 'manufacturer': 'AMD',
             'is_hit': True},
            # Бюджетные
            {'name': 'NVIDIA GeForce RTX 3050 8GB', 'category': 'Видеокарты', 'price': 24990, 'manufacturer': 'NVIDIA',
             'is_hit': False},
            {'name': 'AMD Radeon RX 6400 4GB', 'category': 'Видеокарты', 'price': 14990, 'manufacturer': 'AMD',
             'is_hit': False},

            # ===== МАТЕРИНСКИЕ ПЛАТЫ (15 шт) =====
            # AMD AM5
            {'name': 'ASUS ROG CROSSHAIR X670E HERO', 'category': 'Материнские платы', 'price': 74990,
             'manufacturer': 'ASUS', 'is_hit': False},
            {'name': 'MSI MEG X670E ACE', 'category': 'Материнские платы', 'price': 69990, 'manufacturer': 'MSI',
             'is_hit': False},
            {'name': 'GIGABYTE X670E AORUS MASTER', 'category': 'Материнские платы', 'price': 64990,
             'manufacturer': 'GIGABYTE', 'is_hit': False},
            {'name': 'ASUS TUF GAMING X670E PLUS', 'category': 'Материнские платы', 'price': 34990,
             'manufacturer': 'ASUS', 'is_hit': True},
            {'name': 'MSI MAG B650 TOMAHAWK WIFI', 'category': 'Материнские платы', 'price': 24990,
             'manufacturer': 'MSI', 'is_hit': True},
            {'name': 'GIGABYTE B650 AORUS ELITE AX', 'category': 'Материнские платы', 'price': 22990,
             'manufacturer': 'GIGABYTE', 'is_hit': True},
            {'name': 'ASRock B650M-HDV/M.2', 'category': 'Материнские платы', 'price': 14990, 'manufacturer': 'ASRock',
             'is_hit': False},
            # Intel LGA1700
            {'name': 'ASUS ROG MAXIMUS Z790 HERO', 'category': 'Материнские платы', 'price': 64990,
             'manufacturer': 'ASUS', 'is_hit': False},
            {'name': 'MSI MPG Z790 CARBON WIFI', 'category': 'Материнские платы', 'price': 54990, 'manufacturer': 'MSI',
             'is_hit': False},
            {'name': 'GIGABYTE Z790 AORUS ELITE AX', 'category': 'Материнские платы', 'price': 34990,
             'manufacturer': 'GIGABYTE', 'is_hit': True},
            {'name': 'ASUS TUF GAMING Z790-PLUS WIFI', 'category': 'Материнские платы', 'price': 29990,
             'manufacturer': 'ASUS', 'is_hit': True},
            {'name': 'MSI PRO B760M-A WIFI DDR4', 'category': 'Материнские платы', 'price': 16990,
             'manufacturer': 'MSI', 'is_hit': True},
            {'name': 'GIGABYTE B760M DS3H DDR4', 'category': 'Материнские платы', 'price': 12990,
             'manufacturer': 'GIGABYTE', 'is_hit': False},
            {'name': 'ASRock H610M-HVS', 'category': 'Материнские платы', 'price': 7990, 'manufacturer': 'ASRock',
             'is_hit': False},
            {'name': 'ASUS PRIME H610M-K D4', 'category': 'Материнские платы', 'price': 8990, 'manufacturer': 'ASUS',
             'is_hit': False},

            # ===== ОПЕРАТИВНАЯ ПАМЯТЬ (12 шт) =====
            # DDR5
            {'name': 'G.Skill Trident Z5 RGB 32GB DDR5 6400MHz', 'category': 'Оперативная память', 'price': 19990,
             'manufacturer': 'G.Skill', 'is_hit': True},
            {'name': 'Corsair Vengeance RGB 32GB DDR5 6000MHz', 'category': 'Оперативная память', 'price': 17990,
             'manufacturer': 'Corsair', 'is_hit': True},
            {'name': 'Kingston Fury Beast 32GB DDR5 5600MHz', 'category': 'Оперативная память', 'price': 14990,
             'manufacturer': 'Kingston', 'is_hit': True},
            {'name': 'TeamGroup T-Force Delta RGB 32GB DDR5 6000MHz', 'category': 'Оперативная память', 'price': 16990,
             'manufacturer': 'TeamGroup', 'is_hit': False},
            {'name': 'ADATA XPG Lancer RGB 32GB DDR5 6000MHz', 'category': 'Оперативная память', 'price': 15990,
             'manufacturer': 'ADATA', 'is_hit': False},
            {'name': 'Crucial Pro 32GB DDR5 5600MHz', 'category': 'Оперативная память', 'price': 13990,
             'manufacturer': 'Crucial', 'is_hit': False},
            # DDR4
            {'name': 'G.Skill Ripjaws V 32GB DDR4 3600MHz', 'category': 'Оперативная память', 'price': 9990,
             'manufacturer': 'G.Skill', 'is_hit': True},
            {'name': 'Corsair Vengeance LPX 32GB DDR4 3200MHz', 'category': 'Оперативная память', 'price': 8990,
             'manufacturer': 'Corsair', 'is_hit': True},
            {'name': 'Kingston Fury Beast 32GB DDR4 3200MHz', 'category': 'Оперативная память', 'price': 7990,
             'manufacturer': 'Kingston', 'is_hit': True},
            {'name': 'TeamGroup T-Force Vulcan Z 16GB DDR4 3200MHz', 'category': 'Оперативная память', 'price': 4990,
             'manufacturer': 'TeamGroup', 'is_hit': False},
            {'name': 'ADATA XPG GAMMIX D10 16GB DDR4 3200MHz', 'category': 'Оперативная память', 'price': 4490,
             'manufacturer': 'ADATA', 'is_hit': False},
            {'name': 'Crucial Ballistix 16GB DDR4 3200MHz', 'category': 'Оперативная память', 'price': 5490,
             'manufacturer': 'Crucial', 'is_hit': False},

            # ===== SSD НАКОПИТЕЛИ (13 шт) =====
            # PCIe 4.0 NVMe
            {'name': 'Samsung 990 PRO 2TB', 'category': 'SSD накопители', 'price': 19990, 'manufacturer': 'Samsung',
             'is_hit': True},
            {'name': 'Samsung 990 PRO 1TB', 'category': 'SSD накопители', 'price': 11990, 'manufacturer': 'Samsung',
             'is_hit': True},
            {'name': 'WD Black SN850X 2TB', 'category': 'SSD накопители', 'price': 17990,
             'manufacturer': 'Western Digital', 'is_hit': False},
            {'name': 'WD Black SN850X 1TB', 'category': 'SSD накопители', 'price': 10990,
             'manufacturer': 'Western Digital', 'is_hit': False},
            {'name': 'Kingston KC3000 2TB', 'category': 'SSD накопители', 'price': 16990, 'manufacturer': 'Kingston',
             'is_hit': True},
            {'name': 'Kingston KC3000 1TB', 'category': 'SSD накопители', 'price': 9990, 'manufacturer': 'Kingston',
             'is_hit': True},
            {'name': 'Crucial T500 2TB', 'category': 'SSD накопители', 'price': 18990, 'manufacturer': 'Crucial',
             'is_hit': False},
            {'name': 'Crucial P3 Plus 2TB', 'category': 'SSD накопители', 'price': 12990, 'manufacturer': 'Crucial',
             'is_hit': False},
            {'name': 'ADATA XPG Gammix S70 Blade 2TB', 'category': 'SSD накопители', 'price': 14990,
             'manufacturer': 'ADATA', 'is_hit': False},
            # PCIe 3.0 / SATA
            {'name': 'Samsung 970 EVO Plus 1TB', 'category': 'SSD накопители', 'price': 8990, 'manufacturer': 'Samsung',
             'is_hit': True},
            {'name': 'WD Blue SN570 1TB', 'category': 'SSD накопители', 'price': 6990,
             'manufacturer': 'Western Digital', 'is_hit': True},
            {'name': 'Kingston NV2 1TB', 'category': 'SSD накопители', 'price': 5990, 'manufacturer': 'Kingston',
             'is_hit': True},
            {'name': 'Crucial MX500 1TB SATA', 'category': 'SSD накопители', 'price': 7490, 'manufacturer': 'Crucial',
             'is_hit': False},

            # ===== БЛОКИ ПИТАНИЯ (10 шт) =====
            {'name': 'Seasonic PRIME TX-1000 1000W', 'category': 'Блоки питания', 'price': 29990,
             'manufacturer': 'Seasonic', 'is_hit': False},
            {'name': 'Seasonic FOCUS GX-850 850W', 'category': 'Блоки питания', 'price': 16990,
             'manufacturer': 'Seasonic', 'is_hit': True},
            {'name': 'be quiet! Dark Power 13 1000W', 'category': 'Блоки питания', 'price': 27990,
             'manufacturer': 'be quiet!', 'is_hit': False},
            {'name': 'be quiet! Pure Power 12 M 750W', 'category': 'Блоки питания', 'price': 12990,
             'manufacturer': 'be quiet!', 'is_hit': True},
            {'name': 'Corsair RM1000x 1000W', 'category': 'Блоки питания', 'price': 19990, 'manufacturer': 'Corsair',
             'is_hit': True},
            {'name': 'Corsair RM850e 850W', 'category': 'Блоки питания', 'price': 14990, 'manufacturer': 'Corsair',
             'is_hit': True},
            {'name': 'Corsair CX650 650W', 'category': 'Блоки питания', 'price': 7990, 'manufacturer': 'Corsair',
             'is_hit': False},
            {'name': 'NZXT C850 850W', 'category': 'Блоки питания', 'price': 14990, 'manufacturer': 'NZXT',
             'is_hit': False},
            {'name': 'DeepCool PQ850M 850W', 'category': 'Блоки питания', 'price': 11990, 'manufacturer': 'DeepCool',
             'is_hit': False},
            {'name': 'Chieftec Proton 750W', 'category': 'Блоки питания', 'price': 6990, 'manufacturer': 'Chieftec',
             'is_hit': False},

            # ===== ОХЛАЖДЕНИЕ (10 шт) =====
            # Жидкостное
            {'name': 'NZXT Kraken Elite 360', 'category': 'Охлаждение', 'price': 24990, 'manufacturer': 'NZXT',
             'is_hit': True},
            {'name': 'NZXT Kraken X63 280mm', 'category': 'Охлаждение', 'price': 16990, 'manufacturer': 'NZXT',
             'is_hit': False},
            {'name': 'Arctic Liquid Freezer III 360', 'category': 'Охлаждение', 'price': 16990,
             'manufacturer': 'Arctic', 'is_hit': True},
            {'name': 'Arctic Liquid Freezer II 240', 'category': 'Охлаждение', 'price': 9990, 'manufacturer': 'Arctic',
             'is_hit': False},
            {'name': 'DeepCool LS720 360mm', 'category': 'Охлаждение', 'price': 14990, 'manufacturer': 'DeepCool',
             'is_hit': False},
            {'name': 'DeepCool AK620', 'category': 'Охлаждение', 'price': 6990, 'manufacturer': 'DeepCool',
             'is_hit': True},
            # Воздушное
            {'name': 'Noctua NH-D15', 'category': 'Охлаждение', 'price': 11990, 'manufacturer': 'Noctua',
             'is_hit': True},
            {'name': 'Noctua NH-U12S', 'category': 'Охлаждение', 'price': 7990, 'manufacturer': 'Noctua',
             'is_hit': False},
            {'name': 'be quiet! Dark Rock Pro 4', 'category': 'Охлаждение', 'price': 9990, 'manufacturer': 'be quiet!',
             'is_hit': False},
            {'name': 'ID-COOLING SE-214-XT', 'category': 'Охлаждение', 'price': 2490, 'manufacturer': 'ID-COOLING',
             'is_hit': True},

            # ===== КОРПУСА (5 шт) =====
            {'name': 'NZXT H9 Flow', 'category': 'Корпуса', 'price': 16990, 'manufacturer': 'NZXT', 'is_hit': True},
            {'name': 'Lian Li O11 Dynamic EVO', 'category': 'Корпуса', 'price': 14990, 'manufacturer': 'Lian Li',
             'is_hit': False},
            {'name': 'Fractal Design Meshify 2', 'category': 'Корпуса', 'price': 13990,
             'manufacturer': 'Fractal Design', 'is_hit': False},
            {'name': 'Corsair 4000D Airflow', 'category': 'Корпуса', 'price': 9990, 'manufacturer': 'Corsair',
             'is_hit': True},
            {'name': 'DeepCool CH560', 'category': 'Корпуса', 'price': 6990, 'manufacturer': 'DeepCool',
             'is_hit': False},
        ]

        # === 3. Добавляем компоненты в БД ===
        created_count = 0
        for comp_data in components_data:
            category = categories.get(comp_data['category'])
            if category:
                comp, created = Component.objects.get_or_create(
                    name=comp_data['name'],
                    category=category,
                    defaults={
                        'manufacturer': comp_data['manufacturer'],
                        'price': Decimal(comp_data['price']),
                        'in_stock': True,
                        'is_hit': comp_data.get('is_hit', False),
                    }
                )
                if created:
                    created_count += 1
                    status = '✅ Создан'
                else:
                    status = '⚠️ Уже существует'
                self.stdout.write(f'Компонент: {comp_data["name"]} — {status}')

        # === 4. Итоговый отчёт ===
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS(f'📊 СТАТИСТИКА:'))
        self.stdout.write(self.style.SUCCESS(f'   Категорий: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Компонентов всего: {Component.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Новых добавлено: {created_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        if created_count == 0:
            self.stdout.write(self.style.WARNING('⚠️  Все компоненты уже были в базе!'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ База данных успешно наполнена!'))