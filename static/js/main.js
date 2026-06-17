document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('api-product-grid');
    const spinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const toast = document.getElementById('toast-notification');

    
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

async function secureFetch(url, options = {}) {
    options.headers = options.headers || {};

    const method = (options.method || 'GET').toUpperCase();
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
        options.headers['X-CSRFToken'] = getCookie('csrftoken');
        options.credentials = 'include'; 
    }

    try {
        const response = await fetch(url, options);

        if (response.status === 401 || response.status === 403) {
            alert('Сессия истекла или у вас нет прав доступа. Перенаправление на страницу входа...');
            window.location.href = '/login/'; 
            return null;
        }

        return response;
    } catch (error) {
        console.error('Сетевой сбой при защищенном запросе:', error);
        throw error;
    }
}


    function showToast(message, isSuccess = true) {
        toast.innerText = message;
        toast.style.backgroundColor = isSuccess ? '#4e8c53' : '#c45a4a';
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    async function loadProducts() {

        spinner.style.display = 'block';
        productGrid.innerHTML = '';
        errorMessage.style.display = 'none';

        try {
            const response = await fetch('/api/products/');
            
         
            if (!response.ok) {
                throw new Error('Не удалось загрузить товары с сервера');
            }

            const products = await response.json();
            spinner.style.display = 'none';

            if (products.length === 0) {
                productGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #7a6a58;">Товары временно отсутствуют.</p>';
                return;
            }

        
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'product-card';
                
          
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

          
            initCartButtons();

        } catch (error) {
            
            spinner.style.display = 'none';
            errorMessage.innerText = `Ошибка: ${error.message}. Пожалуйста, попробуйте позже.`;
            errorMessage.style.display = 'block';
        }
    }

    function initCartButtons() {
    const buttons = document.querySelectorAll('.add-to-cart-btn');
    buttons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const productId = e.target.getAttribute('data-id');
            
            try {
                const response = await fetch(`/cart/add/${productId}/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
});


                // Выводим цифровой статус ответа (например, 500, 403, 404)
                console.log('Статус ответа сервера:', response.status);
                
                const text = await response.text();
                // Логируем в консоль чистый текст ошибки или HTML-страницу ошибки Django
                console.log('Текст ошибки сервера:', text);

                if (response.ok) {
                    alert('Товар добавлен!');
                } else {
                    alert(`Ошибка сервера! Статус: ${response.status}. Откройте консоль F12.`);
                }
            } catch (error) {
                console.error('Ошибка сети:', error);
            }
        });
    });
}


    loadProducts();
});
