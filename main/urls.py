from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ProductViewSet,
    CategoryViewSet,
    ManufacturerViewSet,
    CartViewSet,
    ElemCartViewSet,
    index,
    product_list,
    product_detail,
    add_to_cart,
    update_cart,
    remove_from_cart,
    cart_view,
    checkout,
    order_success,
    register_view,
    login_view,
    logout_view,
    profile_view,
    settings_view
    
)
from .views import me_view, OrderViewSet
app_name = 'catalog'
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'elem-carts', ElemCartViewSet, basename='elemcart') 
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', product_list, name='product_list'),
    path('catalog/<int:pk>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('api/me/', me_view, name='api_me'),
    path('api/', include(router.urls)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('test/', views.test, name='test'),

]

