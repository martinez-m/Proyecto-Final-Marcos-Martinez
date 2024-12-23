from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm, PedidoForm, CustomUserCreationForm, DetallePedidoForm
from .models import Producto, Pedido, Categoria, DetallePedido
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.forms import modelformset_factory
from decimal import Decimal
from django.core.serializers import serialize
import json

def inicio(request):
    if request.user.is_authenticated:
        return render(request, 'tienda/inicio_autenticado.html')
    return render(request, 'tienda/inicio_publico.html') 

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'tienda/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'tienda/login.html'

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado con éxito.")
            return redirect('listar_productos')  
        else:
            messages.error(request, "Hubo un error al crear el producto.")
    else:
        form = ProductoForm()

    return render(request, 'tienda/crear_producto.html', {'form': form})

@login_required
def crear_pedido(request):
    pedido_form = PedidoForm(usuario_actual=request.user)
    detalle_form = None  

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, usuario_actual=request.user)

        categoria = request.POST.get('categoria')

        if categoria:
            detalle_form = DetallePedidoForm(request.POST, categoria=categoria)  
        else:
            detalle_form = DetallePedidoForm()

        if pedido_form.is_valid() and detalle_form.is_valid():
            producto = detalle_form.cleaned_data['producto']
            cantidad = detalle_form.cleaned_data['cantidad']

            if producto.stock < cantidad:
                messages.error(request, f"No hay suficiente stock de {producto.nombre}. Solo quedan {producto.stock} unidades disponibles.")
                return render(request, 'tienda/crear_pedido.html', {
                    'pedido_form': pedido_form,
                    'detalle_form': detalle_form,
                })

            pedido = pedido_form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            detalle_pedido = detalle_form.save(commit=False)
            detalle_pedido.pedido = pedido
            detalle_pedido.subtotal = producto.precio * cantidad
            detalle_pedido.save()

            producto.stock -= cantidad
            producto.save()

            messages.success(request, "¡Pedido creado con éxito!")
            return redirect('base')
        else:
            messages.error(request, "Por favor, completa todos los campos correctamente.")
    else:
        detalle_form = DetallePedidoForm()
    return render(request, 'tienda/crear_pedido.html', {
        'pedido_form': pedido_form,
        'detalle_form': detalle_form,
    })

def obtener_productos_por_categoria(request):
    categoria_id = request.GET.get('categoria_id')
    productos = Producto.objects.filter(categoria_id=categoria_id)
    productos_data = [{"id": producto.id, "nombre": producto.nombre} for producto in productos]
    return JsonResponse({"productos": productos_data})

def buscar_producto(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query) if query else []  
    return render(request, 'tienda/buscar_producto.html', {'query': query, 'productos': productos})

def listar_productos(request):
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')  
    if categoria_id:  
        productos = Producto.objects.filter(categoria_id=categoria_id)
    else:
        productos = Producto.objects.all()  
    return render(request, 'tienda/listar_productos.html', {
        'categorias': categorias,
        'productos': productos,
        'categoria_seleccionada': categoria_id,  
    })

def about(request):
    return render(request, 'tienda/about.html')