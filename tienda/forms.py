from django import forms
from .models import Producto, Cliente, Pedido
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'productos', 'total'] 
        widgets = {
            'productos': forms.CheckboxSelectMultiple() 
}

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

    def clean(self):
        """
        Validación personalizada para asegurar que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")