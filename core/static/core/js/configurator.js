document.addEventListener('DOMContentLoaded', () => {
    // ========================================
    // CONFIGURATOR STATE
    // ========================================
    const requiredComponents = ['processor', 'motherboard', 'power-supply', 'case', 'cpu-cooler', 'ram', 'storage'];
    let selectedComponents = {};
    let currentCategory = null;
    let selectedTempComponent = null;
    let currentSort = 'name';

    // ========================================
    // MODAL ELEMENTS
    // ========================================
    const modal = document.getElementById('componentModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalClose = document.getElementById('modalClose');
    const modalCancel = document.getElementById('modalCancel');
    const modalConfirm = document.getElementById('modalConfirm');
    const componentsList = document.getElementById('componentsList');
    const componentSearch = document.getElementById('componentSearch');
    const modalSearchInput = document.getElementById('modalSearchInput');
    const filtersReset = document.getElementById('filtersReset');
    const filtersApply = document.getElementById('filtersApply');
    const priceApply = document.getElementById('priceApply');
    const pagination = document.getElementById('pagination');

    // ========================================
    // OPEN MODAL
    // ========================================
    document.querySelectorAll('.component-select-btn, .change-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const category = btn.getAttribute('data-category');
            const componentType = btn.getAttribute('data-component-type') || category;
            openModal(category, componentType);
        });
    });

    // ========================================
    // CANCEL SELECTION BUTTON
    // ========================================
    document.addEventListener('click', (e) => {
        const cancelBtn = e.target.closest('.cancel-selection-btn');
        if (cancelBtn) {
            const category = cancelBtn.getAttribute('data-category');
            cancelComponentSelection(category);
        }
    });

    function cancelComponentSelection(category) {
        // Удаляем компонент из selectedComponents
        delete selectedComponents[category];

        // Находим секцию компонента
        const section = document.querySelector(`.component-section[data-category="${category}"]`);
        if (section) {
            // Убираем класс has-selection
            section.classList.remove('has-selection');

            // Сбрасываем отображение
            const selectBtn = section.querySelector('.component-select-btn');
            const selectedInfo = section.querySelector('.component-selected-info');
            const nameEl = selectedInfo?.querySelector('.selected-component-name');
            const priceEl = selectedInfo?.querySelector('.selected-component-price');

            if (selectBtn) selectBtn.style.display = 'inline-flex';
            if (nameEl) nameEl.textContent = 'Не выбрано';
            if (priceEl) priceEl.textContent = '0 ₽';
        }

        // Обновляем общую сумму и прогресс
        updateTotalPrice();
        updateProgress();
    }

    function openModal(category, componentType) {
        currentCategory = category;
        selectedTempComponent = selectedComponents[category] || null;

        // Set modal title
        const categoryNames = {
            'processor': 'Процессоры',
            'motherboard': 'Материнские платы',
            'ram': 'Оперативная память',
            'storage': 'Накопители',
            'gpu': 'Видеокарты',
            'power-supply': 'Блоки питания',
            'case': 'Корпуса',
            'cpu-cooler': 'Кулеры для процессора'
        };

        modalTitle.textContent = `Выбор: ${categoryNames[category] || category}`;

        // Show modal
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        // Load components for this category
        populateManufacturerFilters(componentType);
        loadComponents(componentType);

        // Reset filters
        resetFilters();
    }

    // ========================================
    // CLOSE MODAL
    // ========================================
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        currentCategory = null;
        selectedTempComponent = null;
    }

    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (modalCancel) modalCancel.addEventListener('click', closeModal);

    // Close on backdrop click
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // ========================================
    // LOAD COMPONENTS
    // ========================================
    function loadComponents(componentType, page = 1, filters = {}) {
        if (!componentsList) return;

        // Show loading state
        componentsList.innerHTML = '<div style="text-align: center; padding: 40px; color: #9d9dbf;">Загрузка...</div>';

        // Generate sample data
        const sampleComponents = generateSampleComponents(componentType);

        // Apply filters
        let filtered = applyFilters(sampleComponents);

        // Apply sorting
        filtered = applySorting(filtered, currentSort);

        // Render components
        renderComponents(filtered);

        // Update confirm button
        updateConfirmButton();
    }

    // ========================================
    // GENERATE SAMPLE COMPONENTS
    // ========================================
    function generateSampleComponents(type) {
        const manufacturers = {
            'processor': ['Intel', 'AMD'],
            'motherboard': ['ASUS', 'MSI', 'Gigabyte', 'ASRock'],
            'ram': ['Kingston', 'Corsair', 'G.Skill', 'Crucial'],
            'storage': ['Samsung', 'WD', 'Seagate', 'Kingston'],
            'gpu': ['NVIDIA', 'AMD', 'ASUS', 'MSI'],
            'power-supply': ['Be Quiet', 'Corsair', 'EVGA', 'Seasonic'],
            'case': ['NZXT', 'Fractal Design', 'Corsair', 'Lian Li'],
            'cpu-cooler': ['Noctua', 'Be Quiet', 'Corsair', 'DeepCool']
        };

        const components = [];
        const count = 12;

        for (let i = 1; i <= count; i++) {
            const manufacturer = manufacturers[type][Math.floor(Math.random() * manufacturers[type].length)];
            const inStock = Math.random() > 0.2;
            const price = Math.floor(Math.random() * 50000) + 5000;

            components.push({
                id: i,
                name: `${manufacturer} ${type.charAt(0).toUpperCase() + type.slice(1)} ${i}00X`,
                manufacturer: manufacturer,
                category: type,
                price: price,
                in_stock: inStock,
                specs: `Характеристики ${i}`,
                image: null
            });
        }

        return components;
    }

    // ========================================
    // FILTER FUNCTIONS
    // ========================================
    function applyFilters(components) {
        let filtered = [...components];

        // Search filter
        const searchTerm = (componentSearch?.value || modalSearchInput?.value || '').toLowerCase();
        if (searchTerm) {
            filtered = filtered.filter(c =>
                c.name.toLowerCase().includes(searchTerm) ||
                c.manufacturer.toLowerCase().includes(searchTerm)
            );
        }

        // Price filter
        const priceFrom = document.getElementById('priceFrom')?.value;
        const priceTo = document.getElementById('priceTo')?.value;
        if (priceFrom) {
            filtered = filtered.filter(c => c.price >= parseInt(priceFrom));
        }
        if (priceTo) {
            filtered = filtered.filter(c => c.price <= parseInt(priceTo));
        }

        // Stock filter
        const inStockOnly = document.getElementById('inStockOnly')?.checked;
        if (inStockOnly) {
            filtered = filtered.filter(c => c.in_stock);
        }

        // Manufacturer filter
        const selectedManufacturers = Array.from(document.querySelectorAll('#manufacturerFilters input:checked'))
            .map(cb => cb.value);
        if (selectedManufacturers.length > 0) {
            filtered = filtered.filter(c => selectedManufacturers.includes(c.manufacturer));
        }

        return filtered;
    }

    function applySorting(components, sortType) {
        const sorted = [...components];

        switch(sortType) {
            case 'price_asc':
                sorted.sort((a, b) => a.price - b.price);
                break;
            case 'price_desc':
                sorted.sort((a, b) => b.price - a.price);
                break;
            case 'rating':
                // Random for demo
                sorted.sort(() => Math.random() - 0.5);
                break;
            case 'stock':
                sorted.sort((a, b) => (b.in_stock === a.in_stock) ? 0 : b.in_stock ? 1 : -1);
                break;
            case 'name':
            default:
                sorted.sort((a, b) => a.name.localeCompare(b.name));
                break;
        }

        return sorted;
    }

    // ========================================
    // RENDER COMPONENTS
    // ========================================
    function renderComponents(components) {
        if (!componentsList) return;

        componentsList.innerHTML = '';

        if (components.length === 0) {
            componentsList.innerHTML = `
                <div class="no-results" style="text-align: center; padding: 40px; color: #9d9dbf; grid-column: 1/-1;">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="48" height="48" style="margin: 0 auto 15px; opacity: 0.5;">
                        <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                    </svg>
                    <p>Компоненты не найдены</p>
                    <button class="btn" onclick="resetFilters()" style="margin-top: 15px;">Сбросить фильтры</button>
                </div>
            `;
            return;
        }

        components.forEach(component => {
            const item = document.createElement('div');
            item.className = 'component-list-item';
            item.style.cssText = `
                background: rgba(35, 35, 70, 0.6);
                border: 2px solid rgba(157, 78, 221, 0.3);
                border-radius: 12px;
                padding: 18px;
                display: flex;
                gap: 20px;
                align-items: center;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 15px;
            `;

            if (selectedTempComponent && selectedTempComponent.id === component.id) {
                item.classList.add('selected');
                item.style.borderColor = '#10b981';
                item.style.background = 'rgba(20, 40, 30, 0.7)';
            }

            item.innerHTML = `
                <div class="list-item-image" style="flex-shrink: 0; width: 100px; height: 100px; background: linear-gradient(135deg, rgba(157, 78, 221, 0.3) 0%, rgba(99, 102, 241, 0.3) 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 700; color: #ffffff; border: 2px solid rgba(157, 78, 221, 0.5);">
                    ${component.manufacturer.substring(0, 2)}
                </div>
                <div class="list-item-info" style="flex: 1; min-width: 0;">
                    <div class="list-item-name" style="font-size: 1.15rem; color: #ffffff; font-weight: 700; margin-bottom: 8px;">${component.name}</div>
                    <div class="list-item-specs" style="color: #9d9dbf; font-size: 0.9rem; line-height: 1.5; margin-bottom: 8px;">${component.specs}</div>
                    <div class="list-item-stock ${component.in_stock ? '' : 'out-of-stock'}" style="font-size: 0.85rem; color: ${component.in_stock ? '#10b981' : '#ff5252'}; font-weight: 600;">
                        ${component.in_stock ? '✓ в наличии' : '✗ ожидается'}
                    </div>
                </div>
                <div class="list-item-price-action" style="flex-shrink: 0; display: flex; flex-direction: column; gap: 12px; align-items: flex-end;">
                    <div class="list-item-price" style="font-size: 1.4rem; color: #10b981; font-weight: 700;">${component.price.toLocaleString('ru-RU')} ₽</div>
                    <button class="list-item-select-btn" data-id="${component.id}" style="background: linear-gradient(135deg, #9d4edd 0%, #7e3cc5 100%); color: #ffffff; border: none; border-radius: 8px; padding: 10px 24px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase;">Выбрать</button>
                </div>
            `;

            // Click on entire item
            item.addEventListener('click', (e) => {
                if (!e.target.classList.contains('list-item-select-btn')) {
                    selectComponentInModal(component, item);
                }
            });

            // Click on select button
            const selectBtn = item.querySelector('.list-item-select-btn');
            selectBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                selectComponentInModal(component, item);
            });

            componentsList.appendChild(item);
        });
    }

    // ========================================
    // SELECT COMPONENT IN MODAL
    // ========================================
    function selectComponentInModal(component, itemElement) {
        // Remove previous selection
        document.querySelectorAll('.component-list-item.selected').forEach(c => {
            c.classList.remove('selected');
            c.style.borderColor = 'rgba(157, 78, 221, 0.3)';
            c.style.background = 'rgba(35, 35, 70, 0.6)';
        });

        // Add new selection
        itemElement.classList.add('selected');
        itemElement.style.borderColor = '#10b981';
        itemElement.style.background = 'rgba(20, 40, 30, 0.7)';
        selectedTempComponent = component;

        // Update confirm button
        updateConfirmButton();
    }

    function updateConfirmButton() {
        if (modalConfirm) {
            modalConfirm.disabled = !selectedTempComponent;
            modalConfirm.style.opacity = selectedTempComponent ? '1' : '0.5';
        }
    }

    // ========================================
    // CONFIRM SELECTION
    // ========================================
    if (modalConfirm) {
        modalConfirm.addEventListener('click', () => {
            if (selectedTempComponent && currentCategory) {
                // Save selection
                selectedComponents[currentCategory] = selectedTempComponent;

                // Update UI in configurator
                updateComponentSection(currentCategory, selectedTempComponent);

                // Update total price and progress
                updateTotalPrice();
                updateProgress();

                // Close modal
                closeModal();
            }
        });
    }

    // ========================================
    // UPDATE COMPONENT SECTION
    // ========================================
    function updateComponentSection(category, component) {
        const section = document.querySelector(`.component-section[data-category="${category}"]`);
        if (!section) return;

        const selectBtn = section.querySelector('.component-select-btn');
        const selectedInfo = section.querySelector('.component-selected-info');
        if (!selectedInfo) return;

        const nameEl = selectedInfo.querySelector('.selected-component-name');
        const priceEl = selectedInfo.querySelector('.selected-component-price');

        if (nameEl) nameEl.textContent = component.name;
        if (priceEl) priceEl.textContent = `${component.price.toLocaleString('ru-RU')} ₽`;

        section.classList.add('has-selection');
    }

    // ========================================
    // UPDATE TOTAL PRICE
    // ========================================
    function updateTotalPrice() {
        let total = 0;
        let count = 0;

        Object.values(selectedComponents).forEach(component => {
            total += component.price;
            count++;
        });

        const totalPriceEl = document.querySelector('.total-price-value');
        const totalItemsEl = document.querySelector('.total-items-count');

        if (totalPriceEl) {
            totalPriceEl.textContent = `${total.toLocaleString('ru-RU')} ₽`;
        }

        if (totalItemsEl) {
            totalItemsEl.innerHTML = `Добавлено товаров <strong>${count} шт.</strong>`;
        }
    }

    // ========================================
    // UPDATE PROGRESS
    // ========================================
    function updateProgress() {
        const selectedRequired = Object.keys(selectedComponents).filter(key =>
            requiredComponents.includes(key)
        ).length;

        const requiredPercent = Math.round((selectedRequired / requiredComponents.length) * 100);

        const requiredBar = document.querySelector('.progress-bar-fill');
        if (requiredBar) {
            requiredBar.style.width = `${requiredPercent}%`;
            const text = requiredBar.querySelector('.progress-bar-text');
            if (text) text.textContent = `${requiredPercent}%`;
        }
    }

    // ========================================
    // POPULATE MANUFACTURER FILTERS
    // ========================================
    function populateManufacturerFilters(type) {
        const manufacturers = {
            'processor': ['Intel', 'AMD'],
            'motherboard': ['ASUS', 'MSI', 'Gigabyte', 'ASRock'],
            'ram': ['Kingston', 'Corsair', 'G.Skill', 'Crucial'],
            'storage': ['Samsung', 'WD', 'Seagate', 'Kingston'],
            'gpu': ['NVIDIA', 'AMD', 'ASUS', 'MSI'],
            'power-supply': ['Be Quiet', 'Corsair', 'EVGA', 'Seasonic'],
            'case': ['NZXT', 'Fractal Design', 'Corsair', 'Lian Li'],
            'cpu-cooler': ['Noctua', 'Be Quiet', 'Corsair', 'DeepCool']
        };

        const container = document.getElementById('manufacturerFilters');
        if (!container) return;

        container.innerHTML = '';

        (manufacturers[type] || []).forEach(manufacturer => {
            const label = document.createElement('label');
            label.className = 'checkbox-label';
            label.style.cssText = 'display: flex; align-items: center; gap: 10px; color: #b0b0d0; cursor: pointer; position: relative; padding-left: 28px;';
            label.innerHTML = `
                <input type="checkbox" value="${manufacturer}" style="position: absolute; opacity: 0; cursor: pointer;">
                <span class="checkmark" style="position: absolute; left: 0; top: 50%; transform: translateY(-50%); height: 18px; width: 18px; background: rgba(30, 30, 60, 0.8); border: 1px solid rgba(157, 78, 221, 0.4); border-radius: 4px;"></span>
                ${manufacturer}
            `;

            const checkbox = label.querySelector('input');
            checkbox.addEventListener('change', () => {
                loadComponents(currentCategory);
            });

            container.appendChild(label);
        });
    }

    // ========================================
    // RESET FILTERS
    // ========================================
    function resetFilters() {
        if (componentSearch) componentSearch.value = '';
        if (modalSearchInput) modalSearchInput.value = '';
        const priceFrom = document.getElementById('priceFrom');
        const priceTo = document.getElementById('priceTo');
        if (priceFrom) priceFrom.value = '';
        if (priceTo) priceTo.value = '';
        const inStockOnly = document.getElementById('inStockOnly');
        if (inStockOnly) inStockOnly.checked = true;
        document.querySelectorAll('#manufacturerFilters input').forEach(cb => {
            cb.checked = false;
        });

        if (currentCategory) {
            loadComponents(currentCategory);
        }
    }

    if (filtersReset) filtersReset.addEventListener('click', resetFilters);
    if (filtersApply) filtersApply.addEventListener('click', () => loadComponents(currentCategory));

    // ========================================
    // SORT BUTTONS
    // ========================================
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentSort = btn.getAttribute('data-sort');
            loadComponents(currentCategory);
        });
    });

    // ========================================
    // SEARCH INPUTS
    // ========================================
    if (componentSearch) {
        componentSearch.addEventListener('input', () => loadComponents(currentCategory));
    }
    if (modalSearchInput) {
        modalSearchInput.addEventListener('input', () => {
            if (componentSearch) componentSearch.value = modalSearchInput.value;
            loadComponents(currentCategory);
        });
    }

    // ========================================
    // INITIALIZATION
    // ========================================
    function init() {
        updateTotalPrice();
        updateProgress();
    }

    init();
});