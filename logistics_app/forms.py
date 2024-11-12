from django import forms
from .models import Client, Ship, Cargo, Route, Pier

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
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 3}),
        }
