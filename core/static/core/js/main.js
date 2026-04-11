// SpecBox - Навигация и логика корзины
document.addEventListener('DOMContentLoaded', () => {
    console.log('SpecBox загружен');

    // Инициализация счетчика корзины при загрузке
    updateCartBadge();

    // Активация навигации
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Обработка кнопок добавления в корзину
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn:not(.disabled)');

    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            // Находим карточку товара
            const card = this.closest('.component-card, .cart-item');
            if (!card) return;

            // Собираем данные о товаре
            const nameEl = card.querySelector('.component-name, h3');
            const priceEl = card.querySelector('.price-value');
            const categoryEl = card.querySelector('.component-category');
            const manufacturerEl = card.querySelector('.component-manufacturer');

            const name = nameEl ? nameEl.textContent.trim() : 'Товар';
            const priceText = priceEl ? priceEl.textContent : '0';
            const price = parseInt(priceText.replace(/\D/g, '')) || 0;
            const category = categoryEl ? categoryEl.textContent.trim() : '';
            const manufacturer = manufacturerEl ? manufacturerEl.textContent.trim() : '';

            // Получаем ID из data-атрибута или генерируем временный
            const id = this.dataset.id || Date.now();

            // Добавляем в корзину
            addToCart(name, price, id, category, manufacturer);

            // Визуальный эффект
            const originalText = this.textContent;
            this.textContent = '✓ ДОБАВЛЕНО';
            this.style.background = '#10b981';

            setTimeout(() => {
                this.textContent = originalText;
                this.style.background = '';
            }, 1500);
        });
    });

    // Кнопка сброса фильтров
    const resetBtn = document.querySelector('.filters-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            document.querySelectorAll('.filter-checkboxes input').forEach(cb => cb.checked = false);
            document.querySelectorAll('.price-from, .price-to, .filter-search').forEach(input => input.value = '');
            const range = document.querySelector('.price-range');
            if (range) range.value = 200000;
            alert('Фильтры сброшены');
        });
    }

    // Кнопка применения фильтров
    const applyBtn = document.querySelector('.filter-apply-btn');
    if (applyBtn) {
        applyBtn.addEventListener('click', function() {
            const checkedCategories = document.querySelectorAll('.filter-checkboxes input[name="category"]:checked').length;
            const checkedBrands = document.querySelectorAll('.filter-checkboxes input[name="brand"]:checked').length;
            alert('Фильтры применены!\nКатегорий: ' + checkedCategories + '\nБрендов: ' + checkedBrands);
        });
    }
});

// ==========================================
// ГЛОБАЛЬНАЯ ФУНКЦИЯ ДОБАВЛЕНИЯ В КОРЗИНУ
// ==========================================
window.addToCart = function(name, price, id, category, manufacturer) {
    // Получаем текущую корзину
    let cart = JSON.parse(localStorage.getItem('specbox_cart') || '[]');

    // Проверяем, есть ли уже такой товар
    const existingItem = cart.find(item => item.id == id);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: price,
            category: category,
            manufacturer: manufacturer,
            quantity: 1
        });
    }

    // Сохраняем в localStorage
    localStorage.setItem('specbox_cart', JSON.stringify(cart));

    // Обновляем счетчик в шапке
    updateCartBadge();

    console.log('✅ Товар добавлен:', name);
    console.log('🛒 Корзина:', cart);
};

// ==========================================
// ОБНОВЛЕНИЕ СЧЕТЧИКА В ШАПКЕ
// ==========================================
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('specbox_cart') || '[]');
    const badge = document.getElementById('headerCartBadge');

    if (badge) {
        const count = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    }
}