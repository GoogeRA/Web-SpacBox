from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('configurator/', views.configurator_view, name='configurator'),
    path('components/', views.components, name='components'),
    path('profile/', views.profile_view, name='profile'),
    path('registration/login', views.login_view, name='login'),
    path('registration/logout/', views.logout_view, name='logout'),
    path('registration/register/', views.register_view, name='register'),
    path('component/<int:component_id>/', views.component_detail_view, name='component_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('compare/', views.compare_view, name='compare'),
    path('compare/manage/', views.compare_manage, name='compare_manage'),
]