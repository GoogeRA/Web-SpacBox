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
    path('registration/register/', views.register_view, name='register')]