from django import forms
from .models import Producto, Pedido, DetallePedido, Categoria
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(), 
        required=True, 
        label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Pedido
        fields = ['usuario', 'categoria']
    def __init__(self, *args, **kwargs):
        usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)
        if usuario_actual:
            self.fields['usuario'].queryset = self.fields['usuario'].queryset.filter(id=usuario_actual.id)

class DetallePedidoForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(), 
        required=True, 
        label="Selecciona un producto"
    )
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        categoria = kwargs.pop('categoria', None)
        super().__init__(*args, **kwargs)
        if categoria:
            self.fields['producto'].queryset = Producto.objects.filter(categoria=categoria)
        else:
            self.fields['producto'].queryset = Producto.objects.none()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir contraseña'}),
        label="Confirmar Contraseña"
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
        label="Nombre"
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
        label="Apellido"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        label="Correo Electrónico"
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        label="Usuario"
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento', 'type': 'date'}),
        label="Fecha de Nacimiento"
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'birth_date', 'password']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso. Por favor, elige otro.")
        return username

    def clean(self):
        """
        Validación personalizada para asegurar que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        """
        Sobrescribir el método save para guardar el usuario con una contraseña encriptada.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user