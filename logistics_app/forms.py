from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django import forms
from .models import CustomUser, Client, Ship, Cargo, Route, Pier


class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="First Name", max_length=30, required=True)
    last_name = forms.CharField(label="Last Name", max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[('client', 'Client'), ('director', 'Director'), ('manager', 'Manager')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']

        if commit:
            user.save()

        # Назначаем роль пользователю, используя группу в Django
        group = Group.objects.get(name=role)
        user.groups.add(group)

        return user


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'tax_id_number', 'client_account', 'street', 'city', 'status', 'bank']
        labels = {
            'name': 'Название клиента',
            'tax_id_number': 'ИНН',
            'client_account': 'Номер счета',
            'street': 'Улица',
            'city': 'Город',
            'status': 'Статус',
            'bank': 'Банк'
        }

class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['registration_number', 'name', 'capacity', 'year_built', 'photo', 'home_port', 'ship_type', 'crew_captain']
        labels = {
            'registration_number': 'Регистрационный номер',
            'name': 'Название',
            'capacity': 'Грузоподъемность',
            'year_built': 'Год постройки',
            'photo': 'Фото',
            'home_port': 'Порт приписки',
            'ship_type': 'Тип судна',
            'crew_captain': 'Капитан'
        }

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['name', 'description', 'declared_value', 'unit_of_measurement', 'insured_value']
        labels = {
            'name': 'Название груза',
            'description': 'Описание',
            'declared_value': 'Объявленная стоимость',
            'unit_of_measurement': 'Единица измерения',
            'insured_value': 'Страховая стоимость'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['departure_date', 'arrival_date']
        labels = {
            'departure_date': 'Дата отправления',
            'arrival_date': 'Дата прибытия'
        }
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PierForm(forms.ModelForm):
    class Meta:
        model = Pier
        fields = ['route', 'port', 'purpose']
        labels = {
            'route': 'Маршрут',
            'port': 'Порт',
            'purpose': 'Назначение'
        }
        
