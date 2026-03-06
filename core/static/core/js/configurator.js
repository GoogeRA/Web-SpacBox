document.addEventListener('DOMContentLoaded', () => {
    // Обработка добавления компонентов
    const componentItems = document.querySelectorAll('.component-item');
    const addButtons = document.querySelectorAll('.btn');
    const statusElement = document.querySelector('.status');
    const requiredComponents = ['processor', 'motherboard', 'power-supply', 'case', 'cpu-cooler', 'ram', 'storage'];
    let selectedComponents = [];

    // Обновление статуса
    function updateStatus() {
        const selectedRequired = selectedComponents.filter(component =>
            requiredComponents.includes(component)
        ).length;

        statusElement.textContent = `${selectedRequired}/${requiredComponents.length}`;

        // Проверка, все ли обязательные компоненты выбраны
        if (selectedRequired === requiredComponents.length) {
            document.querySelector('.btn-lg.btn-primary').style.backgroundColor =
                'linear-gradient(135deg, #5a43a0 0%, #4a338c 100%)';
            document.querySelector('.btn-lg.btn-primary').style.cursor = 'pointer';
        } else {
            document.querySelector('.btn-lg.btn-primary').style.backgroundColor =
                'linear-gradient(135deg, #7d66c5 0%, #6a55b2 100%)';
            document.querySelector('.btn-lg.btn-primary').style.cursor = 'not-allowed';
        }
    }

    // Добавление/удаление компонента
    function toggleComponent(component) {
        const index = selectedComponents.indexOf(component);
        if (index === -1) {
            selectedComponents.push(component);
        } else {
            selectedComponents.splice(index, 1);
        }

        updateStatus();
    }

    // Обработчики кнопок
    addButtons.forEach(button => {
        button.addEventListener('click', () => {
            const componentItem = button.closest('.component-item');
            const component = componentItem.getAttribute('data-component');

            // Если это обязательный компонент
            if (requiredComponents.includes(component)) {
                if (selectedComponents.includes(component)) {
                    // Удаляем компонент
                    componentItem.classList.remove('selected');
                    button.textContent = 'Выбрать';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn');
                    toggleComponent(component);
                } else {
                    // Добавляем компонент
                    componentItem.classList.add('selected');
                    button.textContent = 'Убрать';
                    button.classList.remove('btn');
                    button.classList.add('btn-primary');
                    toggleComponent(component);
                }
            } else {
                // Для необязательных компонентов
                if (componentItem.classList.contains('selected')) {
                    componentItem.classList.remove('selected');
                    button.textContent = 'Выбрать';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn');
                    toggleComponent(component);
                } else {
                    componentItem.classList.add('selected');
                    button.textContent = 'Убрать';
                    button.classList.remove('btn');
                    button.classList.add('btn-primary');
                    toggleComponent(component);
                }
            }
        });
    });
    //Добавить
    // Инициализация
    updateStatus();
});