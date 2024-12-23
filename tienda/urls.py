from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, obtener_productos_por_categoria
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.inicio, name='base'),
    path('crear-pedido/', views.crear_pedido, name='crear_pedido'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('obtener_productos/', obtener_productos_por_categoria, name='obtener_productos'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]