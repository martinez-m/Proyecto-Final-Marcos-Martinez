from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.inicio, name='base'),
    path('crear-cliente/', views.crear_cliente, name='crear_cliente'),
    path('listar-clientes/', views.listar_clientes, name='listar_clientes'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]