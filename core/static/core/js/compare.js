document.addEventListener('DOMContentLoaded', () => {
    renderComparePage();
});

function getCompareList() {
    return JSON.parse(localStorage.getItem('specbox_compare') || '[]');
}

function saveCompareList(list) {
    localStorage.setItem('specbox_compare', JSON.stringify(list));
    renderComparePage();
}

function addToCompare(product) {
    let list = getCompareList();
    // Проверка, нет ли уже в списке
    if (list.find(p => p.id == product.id)) {
        alert('Этот товар уже в сравнении!');
        return;
    }
    // Ограничение (например, до 4 товаров)
    if (list.length >= 4) {
        alert('Можно сравнивать не более 4 товаров.');
        return;
    }
    list.push(product);
    saveCompareList(list);
    alert('Добавлено к сравнению!');
}

function removeFromCompare(productId) {
    let list = getCompareList();
    list = list.filter(p => p.id != productId);
    saveCompareList(list);
}

function clearCompareList() {
    if(confirm('Очистить список сравнения?')) {
        localStorage.removeItem('specbox_compare');
        renderComparePage();
    }
}

function renderComparePage() {
    const list = getCompareList();
    const container = document.getElementById('compareContainer');
    const emptyState = document.getElementById('emptyState');

    if (list.length === 0) {
        container.innerHTML = '';
        container.appendChild(emptyState);
        emptyState.style.display = 'block';
        return;
    }

    // 1. Собираем все уникальные ключи характеристик из всех товаров
    let allSpecKeys = new Set();
    list.forEach(p => {
        if (p.specifications) {
            Object.keys(p.specifications).forEach(k => allSpecKeys.add(k));
        }
    });
    const specKeys = Array.from(allSpecKeys);

    // 2. Строим таблицу
    let html = '<div class="compare-wrapper"><table class="compare-table"><thead><tr>';

    // Заголовки (первая колонка пустая, далее товары)
    html += '<th>Характеристика</th>';
    list.forEach(p => {
        const initials = p.name.substring(0, 2).toUpperCase();
        html += `
            <th>
                <button class="btn-remove" onclick="removeFromCompare(${p.id})">✕</button>
                <div class="product-card-header">
                    <div class="product-image-placeholder">${initials}</div>
                    <h3 class="product-name">${p.name}</h3>
                    <div class="product-price">${p.price} ₽</div>
                    <div class="${p.in_stock ? 'in-stock' : 'out-stock'}">
                        ${p.in_stock ? 'В наличии' : 'Под заказ'}
                    </div>
                </div>
            </th>
        `;
    });
    html += '</tr></thead><tbody>';

    // Фиксированные строки
    // Цена
    html += `<tr><td>Цена</td>`;
    list.forEach(p => {
        html += `<td style="font-weight:bold; color:#10b981; font-size:1.1rem;">${p.price} ₽</td>`;
    });
    html += `</tr>`;

    // Динамические характеристики
    specKeys.forEach(key => {
        html += `<tr><td>${key}</td>`;

        // Собираем значения для этой характеристики, чтобы найти различия
        let values = list.map(p => (p.specifications && p.specifications[key]) ? p.specifications[key] : '-');
        let isDifferent = new Set(values).size > 1; // Если значений больше 1, значит они разные

        values.forEach(val => {
            html += `<td class="${isDifferent ? 'diff' : ''}">${val}</td>`;
        });
        html += `</tr>`;
    });

    html += '</tbody></table></div>';

    container.innerHTML = html;
}
