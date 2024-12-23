from django.contrib import admin
from .models import Producto, Pedido, Categoria

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Categoria)