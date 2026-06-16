document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('api-product-grid');
    const spinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const toast = document.getElementById('toast-notification');

    // Функция для получения CSRF-токена из куки (необходима для POST-запросов в Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Показывает всплывающее уведомление
    function showToast(message, isSuccess = true) {
        toast.innerText = message;
        toast.style.backgroundColor = isSuccess ? '#4e8c53' : '#c45a4a';
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    // 1. Функция загрузки товаров из API (с поддержкой спиннера и ошибок)
    async function loadProducts() {
        // 4. Показываем спиннер загрузки
        spinner.style.display = 'block';
        productGrid.innerHTML = '';
        errorMessage.style.display = 'none';

        try {
            const response = await fetch('/api/products/');
            
            // 5. Обработка ошибок: если API вернул статус не 200
            if (!response.ok) {
                throw new Error('Не удалось загрузить товары с сервера');
            }

            const products = await response.json();
            spinner.style.display = 'none'; // Скрываем спиннер

            if (products.length === 0) {
                productGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #7a6a58;">Товары временно отсутствуют.</p>';
                return;
            }

            // Рендерим полученные товары динамически
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'product-card';
                
                // Проверяем наличие фото и остатка на складе
                const imgHtml = product.image 
                    ? `<img src="${product.image}" alt="${product.name}" class="product-img">`
                    : `<div class="product-img" style="display: flex; align-items: center; justify-content: center; color: #a89f91; font-size: 0.8rem; background:#fbf9f5; height:180px; border-radius:8px; margin-bottom:15px;">Нет фото</div>`;
                
                const isOutOfStock = product.stock <= 0;
                const buttonText = isOutOfStock ? 'Нет в наличии' : 'В корзину';
                const buttonDisabled = isOutOfStock ? 'disabled' : '';

                card.innerHTML = `
                    <div>
                        ${imgHtml}
                        <h4>${product.name}</h4>
                        <div class="product-price">${product.price} руб.</div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
                        <a href="/catalog/${product.id}/" class="btn-detail">Подробнее</a>
                        <button class="btn-submit add-to-cart-btn" data-id="${product.id}" ${buttonDisabled}>
                            ${buttonText}
                        </button>
                    </div>
                `;
                productGrid.appendChild(card);
            });

            // Навешиваем событие клика на все динамически созданные кнопки "В корзину"
            initCartButtons();

        } catch (error) {
            // 5. Показываем сообщение об ошибке пользователю
            spinner.style.display = 'none';
            errorMessage.innerText = `Ошибка: ${error.message}. Пожалуйста, попробуйте позже.`;
            errorMessage.style.display = 'block';
        }
    }

    // 2. Функция добавления в корзину при нажатии на кнопку
    function initCartButtons() {
        const buttons = document.querySelectorAll('.add-to-cart-btn');
        buttons.forEach(button => {
            button.addEventListener('click', async (e) => {
                const productId = e.target.getAttribute('data-id');
                const csrfToken = getCookie('csrftoken');

                try {
                    // Отправляем POST запрос на указанный в ТЗ эндпоинт
                    const response = await fetch('/api/cart/add/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            product_id: productId,
                            quantity: 1
                        })
                    });

                    if (!response.ok) {
                        throw new Error('Ошибка добавления товара в корзину');
                    }

                    // 3. Уведомление об успешном добавлении
                    showToast('Товар успешно добавлен в корзину! 🐾');

                } catch (error) {
                    showToast(`Не удалось добавить: ${error.message}`, false);
                }
            });
        });
    }

    // Запуск процесса загрузки при открытии страницы
    loadProducts();
});
