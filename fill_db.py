from django.contrib.auth.models import User
from main.models import Product, Category, Manufacturer, Cart, ElemCart
from decimal import Decimal

print("Начинаем заполнение игрушками...")

manufacturers = ['LEGO', 'Hasbro', 'Mattel', 'Playmobil', 'Spin Master']
for name in manufacturers:
    Manufacturer.objects.get_or_create(name=name)
print(f"Производители: {Manufacturer.objects.count()}")

categories = [
    'Конструкторы', 'Мягкие игрушки', 'Машинки и транспорт', 'Куклы и аксессуары',
    'Настольные игры', 'Пазлы', 'Развивающие игрушки', 'Спортивные игрушки',
    'Творчество и наборы', 'Роботы и трансформеры'
]
for name in categories:
    Category.objects.get_or_create(name=name)
print(f"Категории: {Category.objects.count()}")

products = [
    ('Конструктор LEGO City Полицейский участок', 89.90, 15),
    ('Конструктор LEGO Creator 3 в 1 Дом', 65.50, 20),
    ('Конструктор LEGO Technic Гоночный автомобиль', 120.00, 10),
    ('Конструктор LEGO Friends Кафе', 45.80, 18),
    ('Конструктор LEGO Ninjago Храм', 75.30, 12),
    ('Медведь плюшевый 50 см', 42.90, 30),
    ('Кролик мягкий 40 см', 28.50, 25),
    ('Собака плюшевая 60 см', 55.00, 20),
    ('Кот мягкий 35 см', 32.40, 28),
    ('Панда плюшевая 45 см', 48.60, 18),
    ('Радиоуправляемый джип', 85.00, 12),
    ('Железная дорога с поездом', 120.50, 8),
    ('Набор машинок 10 шт', 34.90, 30),
    ('Гоночный трек с машинками', 56.00, 15),
    ('Самолёт на пульте управления', 72.30, 10),
    ('Кукла классическая 30 см', 38.00, 25),
    ('Кукла Барби с аксессуарами', 46.50, 20),
    ('Домик для кукол', 95.00, 8),
    ('Набор одежды для кукол', 22.80, 30),
    ('Коляска для кукол', 32.00, 15),
    ('Монополия классическая', 38.60, 20),
    ('Шахматы деревянные', 28.00, 18),
    ('Карточная игра UNO', 12.90, 40),
    ('Настольный футбол', 65.00, 10),
    ('Домино детское', 14.50, 35),
    ('Пазл 1000 деталей Замок', 22.00, 25),
    ('Пазл 500 деталей Космос', 16.50, 30),
    ('Пазл 3D для детей', 24.80, 20),
    ('Пазл напольный для малышей', 18.00, 22),
    ('Сортер деревянный', 19.60, 30),
    ('Пирамидка детская', 12.40, 40),
    ('Кубики с буквами', 15.80, 35),
    ('Мозаика детская 100 деталей', 21.50, 25),
    ('Мяч футбольный', 18.90, 30),
    ('Баскетбольное кольцо настенное', 34.50, 15),
    ('Набор для рисования 50 предметов', 28.90, 20),
    ('Набор для лепки Play-Doh', 24.00, 25),
    ('Робот трансформер 30 см', 58.60, 12),
    ('Робот на радиоуправлении', 78.00, 8)
]

category_objs = list(Category.objects.all())
manufacturer_objs = list(Manufacturer.objects.all())

for i, (name, price, stock) in enumerate(products):
    Product.objects.get_or_create(
        name=name,
        defaults={
            'price': Decimal(str(price)),
            'stock': stock,
            'category': category_objs[i % len(category_objs)],
            'manufacturer': manufacturer_objs[i % len(manufacturer_objs)]
        }
    )
print(f"Товары: {Product.objects.count()}")

user_names = ['igroman_anna', 'lubitel_pavel', 'kollekcioner_lena', 'gamer_oleg', 'igrushechnik_irina']
for i, name in enumerate(user_names):
    user, created = User.objects.get_or_create(
        username=name,
        defaults={'email': f'user{i+1}@toyshop.by'}
    )
    if created or not user.check_password('toy123'):
        user.set_password('toy123')
        user.save()
print(f"Пользователи: {User.objects.count()}")

try:
    products_list = list(Product.objects.all())
    users_list = list(User.objects.all())

    for idx, user in enumerate(users_list[:5]):
        cart, _ = Cart.objects.get_or_create(user=user)
        try:
            ElemCart.objects.filter(cart=cart).delete()
        except Exception:
            pass
        
        for j in range(3):
            product = products_list[(idx * 4 + j) % len(products_list)]
            quantity = (j + 1) * 2
            try:
                ElemCart.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )
            except Exception:
                pass
except Exception as e:
    print(f"Пропущено заполнение корзин: {e}")

print("\nVSE GOTOVO!")
print(f"Itog:")
print(f"  - Proizvoditeley: {Manufacturer.objects.count()}")
print(f"  - Категорий: {Category.objects.count()}")
print(f"  - Товаров: {Product.objects.count()}")
print(f"  - Пользователей: {User.objects.count()}")
print("\nParol dlya vseh polzovateley: toy123")
print("Loginy: igroman_anna, lubitel_pavel, kollekcioner_lena, gamer_oleg, igrushechnik_irina")
