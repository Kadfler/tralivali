function initStarRating() {
    const stars = document.querySelectorAll('.star-rating .star');
    const ratingInput = document.getElementById('id_rating');

    // Если на этой странице нет звезд (например, зашли на другую вкладку), просто выходим
    if (!stars.length || !ratingInput) return;

    // Функция обновления цвета
    function updateStars(value) {
        stars.forEach(star => {
            if (parseInt(star.getAttribute('data-value')) <= parseInt(value)) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }

    // Инициализация: сразу красим 5 звезд
    updateStars(5);

    // Вешаем клики
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const value = this.getAttribute('data-value');
            ratingInput.value = value; // Передаем цифру в скрытый input
            updateStars(value);        // Перекрашиваем звезды
        });
    });
}

// Запускаем скрипт в зависимости от того, загрузился ли HTML
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStarRating);
} else {
    initStarRating();
}