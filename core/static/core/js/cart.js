document.addEventListener('DOMContentLoaded', () => {
    const STORAGE_KEY = 'specbox_cart';
    const cartWrapper = document.getElementById('cartItemsWrapper');
    const totalItemsCount = document.getElementById('totalItemsCount');
    const subtotalValue = document.getElementById('subtotalValue');
    const totalValue = document.getElementById('totalValue');
    const checkoutBtn = document.getElementById('checkoutBtn');

    // Форматирование цены
    function formatPrice(price) {
        return new Intl.NumberFormat('ru-RU').format(price || 0) + ' ₽';
    }

    // Чтение корзины
    function getCart() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
        } catch (e) {
            console.error('Ошибка чтения корзины:', e);
            return [];
        }
    }

    // Сохранение корзины
    function saveCart(cart) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
        updateHeaderBadge();
        renderCart();
    }

    // Обновление бейджа в шапке
    function updateHeaderBadge() {
        const cart = getCart();
        const badge = document.getElementById('headerCartBadge');
        if (badge) {
            const count = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
            badge.textContent = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }
    }

    // Рендер товаров в корзине
    function renderCart() {
        if (!cartWrapper) return;

        const cart = getCart();
        cartWrapper.innerHTML = ''; // Очищаем текущее содержимое

        if (cart.length === 0) {
            cartWrapper.innerHTML = `
                <div class="empty-cart" style="text-align:center; padding: 50px;">
                    <div class="empty-cart-icon" style="font-size: 4rem; margin-bottom: 20px;">🛒</div>
                    <h3 style="color:#fff; margin-bottom: 10px;">Корзина пуста</h3>
                    <p style="color:#b0b0d0; margin-bottom: 25px;">Добавьте компоненты из каталога или конфигуратора</p>
                    <a href="/components/" class="btn btn-primary">Перейти в каталог</a>
                </div>
            `;
            updateSummary(0, 0);
            return;
        }

        let subtotal = 0;
        let totalCount = 0;

        cart.forEach((item, index) => {
            const qty = item.quantity || 1;
            const lineTotal = item.price * qty;
            subtotal += lineTotal;
            totalCount += qty;

            const el = document.createElement('div');
            el.className = 'cart-item';
            el.style.cssText = "display:flex; justify-content:space-between; align-items:center; padding: 15px; border-bottom: 1px solid rgba(157, 78, 221, 0.2); margin-bottom: 10px;";

            el.innerHTML = `
                <div style="display:flex; align-items:center; gap: 15px; flex:1;">
                    <div style="width:60px; height:60px; background:linear-gradient(135deg, #9d4edd, #6366f1); border-radius:10px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:bold; font-size:1.5rem;">
                        ${(item.name || '?').substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                        <h3 style="margin:0 0 5px; color:#fff; font-size:1.1rem;">${item.name}</h3>
                        <p style="margin:0; color:#b0b0d0; font-size:0.9rem;">${item.category || ''} • ${item.manufacturer || ''}</p>
                        <span style="color:#10b981; font-size:0.8rem; font-weight:600;">✓ В наличии</span>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap: 20px;">
                    <div style="font-size:1.2rem; color:#10b981; font-weight:700; min-width:100px; text-align:right;">
                        ${formatPrice(lineTotal)}
                    </div>
                    <div style="display:flex; align-items:center; background:rgba(30,30,60,0.8); border-radius:8px; padding:2px; border:1px solid rgba(157, 78, 221, 0.3);">
                        <button class="qty-btn" onclick="changeQty(${index}, -1)" style="background:transparent; border:none; color:#fff; padding:5px 10px; cursor:pointer; font-size:1.2rem;">−</button>
                        <span style="padding:0 10px; color:#fff; font-weight:bold; min-width:20px; text-align:center;">${qty}</span>
                        <button class="qty-btn" onclick="changeQty(${index}, 1)" style="background:transparent; border:none; color:#fff; padding:5px 10px; cursor:pointer; font-size:1.2rem;">+</button>
                    </div>
                    <button onclick="removeItem(${index})" style="background:transparent; border:none; color:#ff5252; cursor:pointer; font-size:1.2rem; opacity:0.7; transition:0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.7">🗑️</button>
                </div>
            `;
            cartWrapper.appendChild(el);
        });

        updateSummary(subtotal, totalCount);
    }

    // Обновление итогов
    function updateSummary(subtotal, count) {
        if (totalItemsCount) totalItemsCount.textContent = count;
        if (subtotalValue) subtotalValue.textContent = formatPrice(subtotal);
        if (totalValue) totalValue.textContent = formatPrice(subtotal);
        if (checkoutBtn) checkoutBtn.disabled = count === 0;
    }

    // Глобальные функции для кнопок HTML
    window.changeQty = function(index, change) {
        let cart = getCart();
        if (cart[index]) {
            cart[index].quantity += change;
            if (cart[index].quantity <= 0) {
                cart.splice(index, 1);
            }
            saveCart(cart);
        }
    };

    window.removeItem = function(index) {
        let cart = getCart();
        cart.splice(index, 1);
        saveCart(cart);
    };

    // Кнопка оформления
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            const cart = getCart();
            if (cart.length === 0) return;
            alert('✅ Переход к оформлению заказа!');
        });
    }

    // Запуск при загрузке
    updateHeaderBadge();
    renderCart();
});