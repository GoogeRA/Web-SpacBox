// SpecBox - Навигация и интерактивность
document.addEventListener('DOMContentLoaded', () => {
    console.log('SpecBox загружен');

    // Активация навигации
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

       // Обработка кнопок добавления в сборку
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // 🔥 Важно: не перехватывать клик ссылки
            if (!this.classList.contains('disabled')) {
                const componentName = this.closest('.component-card').querySelector('.component-name').textContent;
                const componentId = this.getAttribute('onclick')?.match(/\d+/)?.[0];

                // Интеграция с конфигуратором (если нужно)
                if (typeof addToBuild === 'function') {
                    addToBuild(componentId, componentName);
                } else {
                    alert('✅ "' + componentName + '" добавлен в сборку!');
                }
            }
        });
    });

    // Кнопка сброса фильтров
    const resetBtn = document.querySelector('.filters-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            document.querySelectorAll('.filter-checkboxes input').forEach(cb => cb.checked = false);
            document.querySelectorAll('.price-from, .price-to, .filter-search').forEach(input => input.value = '');
            document.querySelector('.price-range').value = 200000;
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