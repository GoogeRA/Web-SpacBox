// ========================================
// PROFILE.JS - ФУНКЦИОНАЛ ЛИЧНОГО КАБИНЕТА
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Навигация по секциям
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.profile-section');

    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();

            // Удаляем активный класс у всех
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));

            // Добавляем активный класс текущему
            this.classList.add('active');

            // Показываем соответствующую секцию
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add('active');
            }

            // Сохраняем в localStorage
            localStorage.setItem('activeProfileTab', targetId);
        });
    });

    // Восстанавливаем активную вкладку
    const activeTab = localStorage.getItem('activeProfileTab');
    if (activeTab) {
        const activeNav = document.querySelector(`.nav-item[href="#${activeTab}"]`);
        const activeSection = document.getElementById(activeTab);
        if (activeNav && activeSection) {
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            activeNav.classList.add('active');
            activeSection.classList.add('active');
        }
    }

    // Удаление сборок
    window.deleteBuild = function(buildId) {
        if (confirm('Вы уверены, что хотите удалить эту сборку?')) {
            console.log('Удаление сборки:', buildId);
            alert('Сборка удалена (демо)');
        }
    };

    // Удаление из избранного
    window.removeFavorite = function(favoriteId) {
        if (confirm('Удалить компонент из избранного?')) {
            console.log('Удаление из избранного:', favoriteId);
            alert('Компонент удалён из избранного (демо)');
        }
    };

    // Закрытие уведомлений
    window.closeNotification = function(notificationId) {
        const notification = document.getElementById(`notification-${notificationId}`);
        if (notification) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(20px)';
            setTimeout(() => notification.remove(), 300);
        }
    };

    // Отметить все уведомления как прочитанные
    window.markAllRead = function() {
        document.querySelectorAll('.notification-item.unread').forEach(item => {
            item.classList.remove('unread');
        });
        alert('Все уведомления отмечены как прочитанные');
    };

    // Валидация формы настроек
    const settingsForm = document.querySelector('.settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Настройки сохранены (демо)');
        });
    }

    // Анимация появления элементов
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.build-card, .component-card, .info-card, .notification-item').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.4s ease';
        observer.observe(card);
    });
});