from django.shortcuts import render, redirect
from .forms import ProductoForm, ClienteForm, PedidoForm, CustomUserCreationForm
from .models import Producto, Cliente, Pedido, Categoria
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

def inicio(request):
    if request.user.is_authenticated:
        return render(request, 'tienda/inicio_autenticado.html')  # Usuario autenticado
    return render(request, 'tienda/inicio_publico.html')  # Usuario no autenticado

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
            return redirect('tienda/login')
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
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el producto en la base de datos
            messages.success(request, "Producto creado con éxito.")  # Mostrar mensaje de éxito
        else:
            messages.error(request, "Hubo un error al crear el producto. Revisa los datos ingresados.")
    else:
        form = ProductoForm()

    return render(request, 'tienda/crear_producto.html', {'form': form})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensaje de éxito
            messages.success(request, "¡Cliente creado exitosamente!")
            return redirect('base')  # Redirige al inicio
    else:
        form = ClienteForm()
    return render(request, 'tienda/crear_cliente.html', {'form': form})

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Pedido creado correctamente!')
            return redirect('base')  # Cambia la redirección si prefieres otro destino
    else:
        form = PedidoForm()
    return render(request, 'tienda/crear_pedido.html', {'form': form})

def buscar_producto(request):
    query = request.GET.get('q', '')  # Obtiene el parámetro 'q' de la URL
    productos = Producto.objects.filter(nombre__icontains=query) if query else []  # Filtra productos que contienen el texto
    return render(request, 'tienda/buscar_producto.html', {'query': query, 'productos': productos})

def listar_productos(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    return render(request, 'tienda/listar_productos.html', {'categorias': categorias, 'productos': productos})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'tienda/listar_clientes.html', {'clientes': clientes})

def home(request):
    return render(request, 'tienda/home.html')

def about(request):
    return render(request, 'tienda/about.html')

def productos(request):
    return render(request, 'tienda/productos.html')

def login_view(request):
    return render(request, 'tienda/login.html')


def profile(request):
    return render(request, 'tienda/profile.html')

def logout_view(request):
    # Aquí irá el logout
    pass