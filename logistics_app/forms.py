from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django import forms
from .models import Client, Ship, Cargo, Route, Pier, Bank, City, Crew, Port, Service, Shiptype
from .models import CustomUser, Status, Street, Cargobatch, Unitofmeasurement, Summary, Transportation


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        labels = {
            'username': 'Логин',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('director', 'Директор'),
        ('manager', 'Менеджер'),
        ('client', 'Клиент'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


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
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ShipForm, self).__init__(*args, **kwargs)
        # Фильтруем только сотрудников из экипажа
        self.fields['crew_captain'].queryset = Crew.objects.filter(post='Капитан')

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['name', 'description', 'declared_value', 'unit_of_measurement', 'insured_value']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'declared_value': 'Заявленная величина',
            'unit_of_measurement': 'Ед. измерения',
            'insured_value': 'Застрахованная величина'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'unit_of_measurement': forms.Select(attrs={'class': 'form-control'}),
        }

        

        def clean_declared_value(self):
            value = self.cleaned_data.get('declared_value')
            if isinstance(value, str):
                value = value.replace(',', '.')
            try:
                return float(value)
            except ValueError:
                raise forms.ValidationError("Пожалуйста, введите корректное вещественное число.")

        def clean_insured_value(self):
            value = self.cleaned_data.get('insured_value')
            if isinstance(value, str):
                value = value.replace(',', '.')
            try:
                return float(value)
            except ValueError:
                raise forms.ValidationError("Пожалуйста, введите корректное вещественное число.")

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

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name']
        labels = {
            'name': 'Название'
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        labels = {
            'name': 'Название'
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Название'
        }

class StreetForm(forms.ModelForm):
    class Meta:
        model = Street
        fields = ['name']
        labels = {
            'name': 'Название'
        }

class CargoBatchForm(forms.ModelForm):
    class Meta:
        model = Cargobatch
        fields = ['number_declaration', 'departure_date', 'arrival_date', 'ship', 'port_of_departure', 'port_of_arrival', 'client_recipient', 'client_sender', 'customs_number']
        labels = {
            'number_declaration': 'Номер декларации',
            'departure_date': 'Дата отправления',
            'arrival_date': 'Дата прибытия',
            'ship': 'Судно',
            'port_of_departure': 'Порт отправления',
            'port_of_arrival': 'Порт прибытия',
            'client_recipient': 'Клиент-получатель',
            'client_sender': 'Клиент-отправитель',
            'customs_number': 'Таможенный номер'
        }
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ['last_name', 'first_name', 'middle_name', 'post']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'post': 'Должность'
        }

class PortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = ['name', 'coordinates']
        labels = {
            'name': 'Название',
            'coordinates': 'Координаты'
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['ship', 'crew_employee']
        labels = {
            'ship': 'Судно',
            'crew_employee': 'Сотрудник'
        }

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        # Фильтруем только сотрудников из экипажа
        self.fields['crew_employee'].queryset = Crew.objects.filter(post='Сотрудник')

class ShipTypeForm(forms.ModelForm):
    class Meta:
        model = Shiptype
        fields = ['name']
        labels = {
            'name': 'Название'
        }

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['cargo_batch', 'cargo']
        labels = {
            'cargo_batch': 'Партия груза',
            'cargo': 'Груз'
        }

class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = ['ship', 'route']
        labels = {
            'ship': 'Судно',
            'route': 'Маршрут'
        }

class UnitOfMeasurementForm(forms.ModelForm):
    class Meta:
        model = Unitofmeasurement
        fields = ['name']
        labels = {
            'name': 'Название'
        }