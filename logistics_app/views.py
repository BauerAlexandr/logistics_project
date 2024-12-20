from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.db.models.deletion import ProtectedError
from .models import Client, Ship, Cargo, Route, Pier, Bank, City, Crew, Port, Service, Shiptype
from .models import Status, Street, Cargobatch, Unitofmeasurement, Summary, Transportation
from .forms import UserRegistrationForm, UserLoginForm, ClientForm, ShipForm, CargoForm, RouteForm, PierForm
from .forms import BankForm, CargoBatchForm, CityForm, CrewForm, PortForm, ServiceForm, ShipTypeForm
from .forms import StatusForm, StreetForm, SummaryForm, TransportationForm, UnitOfMeasurementForm, UpdateUserForm, UserUpdateForm


@login_required
def user_profile(request):
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            request.user.profile_image = request.FILES['profile_image']
            request.user.save()
            messages.success(request, "Фото профиля обновлено.")
        else:
            messages.error(request, "Пожалуйста, выберите файл.")
        return redirect('user_profile')

    return render(request, 'logistics_app/profile.html', {'user': request.user})


@login_required
def user_settings(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(instance=request.user, data=request.POST)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Данные успешно обновлены!')
                return redirect('user_settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
        
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Обновляем сессию, чтобы пользователь не был разлогинен
                messages.success(request, 'Пароль успешно изменён!')
                return redirect('user_settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'logistics_app/settings.html', {
        'user_form': user_form,
        'password_form': password_form,
    })

@login_required
def debug_view(request):
    return render(request, 'logistics_app/debug.html', {
        'role': request.user.role,
        'groups': request.user.groups.all(),
        'permissions': request.user.get_all_permissions(),
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.role = role
            user.save()

            # Назначаем пользователя в группу
            group = Group.objects.get(name=role)
            user.groups.add(group)

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'logistics_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'logistics_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.role == 'director':
        return redirect('director_dashboard')
    elif request.user.role == 'manager':
        return redirect('manager_dashboard')
    elif request.user.role == 'client':
        return redirect('client_dashboard')
    else:
        return redirect('login')


@login_required
def director_dashboard(request):
    if request.user.role != 'director':
        return redirect('login')
    return render(request, 'logistics_app/director_dashboard.html')


@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('login')
    return render(request, 'logistics_app/client_dashboard.html')


@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('login')
    return render(request, 'logistics_app/manager_dashboard.html')

def index(request):
    return render(request, 'logistics_app/index.html')

# === SHIPS ===
@permission_required('logistics_app.view_ship', raise_exception=True)
def ship_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')   # Порядок сортировки
    query = request.GET.get('q', '')          # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    ships = Ship.objects.select_related('home_port', 'ship_type', 'crew_captain')
    if query:
        ships = ships.filter(
            Q(name__icontains=query) |
            Q(registration_number__icontains=query) |
            Q(capacity__icontains=query) |
            Q(year_built__icontains=query) |
            Q(crew_captain__last_name__icontains=query)
        )
    ships = ships.order_by(sort_by)

    # Пагинация
    paginator = Paginator(ships, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Данные для выпадающих списков
    ports = Port.objects.all()
    ship_types = Shiptype.objects.all()
    captains = Crew.objects.filter(post='Капитан')

    # Форма для добавления корабля
    if request.method == 'POST' and 'add-ship' in request.POST:
        if request.user.has_perm('logistics_app.add_ship'):
            form = ShipForm(request.POST, request.FILES)
            if form.is_valid():
                ship = form.save(commit=False)
                # Обработка загруженного файла
                if 'photo' in request.FILES:
                    photo_file = request.FILES['photo']
                    file_path = default_storage.save(f"ships/{photo_file.name}", ContentFile(photo_file.read()))
                    ship.photo = file_path  # Сохраняем путь к файлу в поле photo
                ship.save()
                messages.success(request, "Корабль успешно добавлен!")
                return redirect('ships_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = ShipForm()

    

    return render(request, 'logistics_app/ships_list.html', {
        'page_obj': page_obj,
        'ships': ships,
        'form': form,
        'ports': ports,
        'ship_types': ship_types,
        'captains': captains,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_ship', raise_exception=True)
def edit_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    if request.method == 'POST':
        form = ShipForm(request.POST, request.FILES, instance=ship)
        if form.is_valid():
            if 'photo' in request.FILES:
                # Если новое фото загружено, добавляем путь "ships/"
                photo_file = request.FILES['photo']
                file_path = default_storage.save(f"ships/{photo_file.name}", ContentFile(photo_file.read()))
                ship.photo = file_path
            form.save()
            messages.success(request, "Корабль успешно обновлён!")
            return redirect('ships_list')
    return redirect('ships_list')


@permission_required('logistics_app.delete_ship', raise_exception=True)
def delete_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    ship.delete()
    messages.success(request, "Корабль успешно удалён!")
    return redirect('ships_list')

@permission_required('logistics_app.change_ship', raise_exception=True)
def edit_ship_photo(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)

    if request.method == 'POST':
        if 'delete-photo' in request.POST:
            # Удаление текущего фото
            if ship.photo:
                default_storage.delete(ship.photo)  # Удаляем файл из хранилища
                ship.photo = None
                ship.save()
                messages.success(request, "Фото удалено.")
        elif 'update-photo' in request.POST and 'photo' in request.FILES:
            # Замена фото
            photo_file = request.FILES['photo']
            file_path = default_storage.save(f"ships/{photo_file.name}", ContentFile(photo_file.read()))
            ship.photo = file_path
            ship.save()
            messages.success(request, "Фото обновлено.")
        return redirect('ships_list')  # Перенаправление на список кораблей

    return redirect('ships_list')



# === CARGO ===
@permission_required('logistics_app.view_cargo', raise_exception=True)
def cargo_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле для сортировки, по умолчанию 'name'
    order = request.GET.get('order', 'asc')    # Порядок сортировки, по умолчанию 'asc'
    query = request.GET.get('q', '')           # Получаем поисковый запрос из строки

    # Обрабатываем направление сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Поиск по ключевым полям
    cargos = Cargo.objects.select_related('unit_of_measurement').all()
    if query:
        cargos = cargos.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(unit_of_measurement__name__icontains=query) |
            Q(declared_value__icontains=query) |
            Q(insured_value__icontains=query)
        )

    # Применяем сортировку
    cargos = cargos.order_by(sort_by)

    units = Unitofmeasurement.objects.all()

    # Пагинация: 10 записей на странице
    paginator = Paginator(cargos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления груза
    if request.method == 'POST' and 'add-cargo' in request.POST:
        if request.user.has_perm('logistics_app.add_cargo'):
            cargo_form = CargoForm(request.POST)
            if cargo_form.is_valid():
                cargo_form.save()
                return redirect('cargo_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        cargo_form = CargoForm()

    return render(request, 'logistics_app/cargo_list.html', {
        'page_obj': page_obj,
        'cargos': cargos,
        'cargo_form': cargo_form,
        'units': units,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,  # Передаём поисковый запрос в шаблон
    })


@permission_required('logistics_app.change_cargo', raise_exception=True)
def edit_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('cargo_list')
    else:
        form = CargoForm(instance=cargo)
    
    return redirect('cargo_list')


@permission_required('logistics_app.delete_cargo', raise_exception=True)
def delete_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    try:
        cargo.delete()
        messages.success(request, f'Груз "{cargo.name}" был успешно удален.')
    except ProtectedError:
        messages.error(request, f'Невозможно удалить груз "{cargo.name}", так как он связан с другими данными.')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')

    return redirect('cargo_list')

# === CLIENT ===
@permission_required('logistics_app.view_client', raise_exception=True)
def clients_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле для сортировки, по умолчанию 'name'
    order = request.GET.get('order', 'asc')    # Порядок сортировки, по умолчанию 'asc'
    query = request.GET.get('q', '')           # Получаем поисковый запрос из строки

    # Обрабатываем направление сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Поиск по ключевым полям
    clients = Client.objects.select_related('street', 'city', 'status', 'bank').all()
    if query:
        clients = clients.filter(
            Q(name__icontains=query) | 
            Q(tax_id_number__icontains=query) |
            Q(client_account__icontains=query) |
            Q(street__name__icontains=query) |
            Q(city__name__icontains=query) |
            Q(status__name__icontains=query) |
            Q(bank__name__icontains=query)
        )

    # Применяем сортировку
    clients = clients.order_by(sort_by)

    streets = Street.objects.all()
    cities = City.objects.all()
    statuses = Status.objects.all()
    banks = Bank.objects.all()
    # Пагинация: 10 записей на странице
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления клиента
    if request.method == 'POST' and 'add-client' in request.POST:
        if request.user.has_perm('logistics_app.add_client'):
            client_form = ClientForm(request.POST)
            if client_form.is_valid():
                client_form.save()
                messages.success(request, "Клиент успешно добавлен!")
                return redirect('clients_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        client_form = ClientForm()

    return render(request, 'logistics_app/clients_list.html', {
        'page_obj': page_obj,
        'clients': clients,
        'client_form': client_form,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,  # Передаём поисковый запрос в шаблон
        'streets': streets,
        'cities': cities,
        'statuses': statuses,
        'banks': banks,
    })


@permission_required('logistics_app.change_client', raise_exception=True)
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Клиент "{client.name}" успешно обновлен!')
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    
    return redirect('clients_list')


@permission_required('logistics_app.delete_client', raise_exception=True)
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    try:
        client.delete()
        messages.success(request, f'Клиент "{client.name}" был успешно удален.')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')
    return redirect('clients_list')


# === ROUTES ===
@permission_required('logistics_app.view_route', raise_exception=True)
def route_list(request):
    sort_by = request.GET.get('sort', 'departure_date')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')             # Порядок сортировки
    query = request.GET.get('q', '')                    # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    routes = Route.objects.all()
    if query:
        routes = routes.filter(
            Q(departure_date__icontains=query) |
            Q(arrival_date__icontains=query)
        )
    routes = routes.order_by(sort_by)

    # Пагинация
    paginator = Paginator(routes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления маршрута
    if request.method == 'POST' and 'add-route' in request.POST:
        if request.user.has_perm('logistics_app.add_route'):
            form = RouteForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Маршрут успешно добавлен!")
                return redirect('routes_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = RouteForm()

    return render(request, 'logistics_app/routes_list.html', {
        'page_obj': page_obj,
        'routes': routes,
        'form': form,
        'current_sort': request.GET.get('sort', 'departure_date'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_route', raise_exception=True)
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно обновлён!")
            return redirect('routes_list')
    return redirect('routes_list')


@permission_required('logistics_app.delete_route', raise_exception=True)
def delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    route.delete()
    messages.success(request, "Маршрут успешно удалён!")
    return redirect('routes_list')

# === REPORTS ===
def reports(request):
    return render(request, 'logistics_app/reports.html')

# === PIERS ===
@permission_required('logistics_app.view_pier', raise_exception=True)
def pier_list(request):
    sort_by = request.GET.get('sort', 'port__name')  # Поле сортировки, по умолчанию порт
    order = request.GET.get('order', 'asc')          # Порядок сортировки
    query = request.GET.get('q', '')                 # Поисковый запрос

    # Обрабатываем направление сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Получаем список пирсов
    piers = Pier.objects.select_related('route', 'port').all()

    # Поиск по маршруту, порту и назначению
    if query:
        piers = piers.filter(
            Q(route__departure_date__icontains=query) | 
            Q(port__name__icontains=query) | 
            Q(purpose__icontains=query)
        )

    # Сортировка
    piers = piers.order_by(sort_by)

    routes = Route.objects.all()
    ports = Port.objects.all()

    # Пагинация
    paginator = Paginator(piers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления пирса
    if request.method == 'POST' and 'add-pier' in request.POST:
        if request.user.has_perm('logistics_app.add_pier'):
            pier_form = PierForm(request.POST)
            if pier_form.is_valid():
                pier_form.save()
                messages.success(request, "Пирс успешно добавлен!")
                return redirect('piers_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        pier_form = PierForm()

    return render(request, 'logistics_app/piers_list.html', {
        'page_obj': page_obj,
        'pier_form': pier_form,
        'query': query,
        'current_sort': request.GET.get('sort', 'port__name'),
        'current_order': order,
        'routes': routes,
        'ports': ports,
    })

# Редактирование пирса
@permission_required('logistics_app.change_pier', raise_exception=True)
def edit_pier(request, pier_id):
    pier = get_object_or_404(Pier, id=pier_id)
    if request.method == 'POST':
        form = PierForm(request.POST, instance=pier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пирс успешно обновлён!')
    return redirect('piers_list')

# Удаление пирса
@permission_required('logistics_app.delete_pier', raise_exception=True)
def delete_pier(request, pier_id):
    pier = get_object_or_404(Pier, id=pier_id)
    try:
        pier.delete()
        messages.success(request, f'Пирс "{pier}" успешно удалён.')
    except Exception as e:
        messages.error(request, f'Ошибка удаления пирса: {e}')
    return redirect('piers_list')

# === BANK ===
@permission_required('logistics_app.view_bank', raise_exception=True)
def bank_list(request):
    sort_by = request.GET.get('sort', 'name')  # Сортировка по умолчанию
    order = request.GET.get('order', 'asc')    # Направление сортировки
    query = request.GET.get('q', '')           # Поиск по названию банка

    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Поиск по названию банка
    banks = Bank.objects.all()
    if query:
        banks = banks.filter(Q(name__icontains=query))

    # Применяем сортировку
    banks = banks.order_by(sort_by)

    # Пагинация: 10 записей на странице
    paginator = Paginator(banks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления банка
    if request.method == 'POST' and 'add-bank' in request.POST:
        if request.user.has_perm('logistics_app.add_bank'):
            bank_form = BankForm(request.POST)
            if bank_form.is_valid():
                bank_form.save()
                messages.success(request, 'Банк успешно добавлен.')
                return redirect('banks_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        bank_form = BankForm()

    return render(request, 'logistics_app/banks_list.html', {
        'page_obj': page_obj,
        'banks': banks,
        'bank_form': bank_form,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_bank', raise_exception=True)
def edit_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            messages.success(request, 'Банк успешно обновлен.')
            return redirect('banks_list')
    return redirect('banks_list')


@permission_required('logistics_app.delete_bank', raise_exception=True)
def delete_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    try:
        bank.delete()
        messages.success(request, 'Банк успешно удален.')
    except Exception as e:
        messages.error(request, f'Ошибка при удалении банка: {str(e)}')
    return redirect('banks_list')

# === CITIES ===
@permission_required('logistics_app.view_city', raise_exception=True)
def city_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле для сортировки
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    if order == 'desc':
        sort_by = f'-{sort_by}'

    cities = City.objects.all()

    # Поиск
    if query:
        cities = cities.filter(name__icontains=query)

    # Сортировка
    cities = cities.order_by(sort_by)

    # Пагинация
    paginator = Paginator(cities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Добавление города
    if request.method == 'POST' and 'add-city' in request.POST:
        if request.user.has_perm('logistics_app.add_city'):
            city_form = CityForm(request.POST)
            if city_form.is_valid():
                city_form.save()
                messages.success(request, "Город успешно добавлен!")
                return redirect('cities_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        city_form = CityForm()

    return render(request, 'logistics_app/cities_list.html', {
        'page_obj': page_obj,
        'city_form': city_form,
        'query': query,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
    })

# Редактирование города
@permission_required('logistics_app.change_city', raise_exception=True)
def edit_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            messages.success(request, 'Город успешно обновлен!')
    return redirect('cities_list')

# Удаление города
@permission_required('logistics_app.delete_city', raise_exception=True)
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    try:
        city.delete()
        messages.success(request, f'Город "{city.name}" успешно удален.')
    except Exception as e:
        messages.error(request, f'Ошибка удаления города: {e}')
    return redirect('cities_list')


# === CREWS ===
@permission_required('logistics_app.view_crew', raise_exception=True)
def crew_list(request):
    sort_by = request.GET.get('sort', 'last_name')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')         # Порядок сортировки
    query = request.GET.get('q', '')                # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    crews = Crew.objects.all()
    if query:
        crews = crews.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(post__icontains=query)
        )
    crews = crews.order_by(sort_by)

    # Пагинация
    paginator = Paginator(crews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления члена экипажа
    if request.method == 'POST' and 'add-crew' in request.POST:
        if request.user.has_perm('logistics_app.add_crew'):
            form = CrewForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Член экипажа успешно добавлен!")
                return redirect('crews_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = CrewForm()

    return render(request, 'logistics_app/crews_list.html', {
        'page_obj': page_obj,
        'crews': crews,
        'form': form,
        'current_sort': request.GET.get('sort', 'last_name'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_crew', raise_exception=True)
def edit_crew(request, crew_id):
    crew = get_object_or_404(Crew, id=crew_id)
    if request.method == 'POST':
        form = CrewForm(request.POST, instance=crew)
        if form.is_valid():
            form.save()
            messages.success(request, "Член экипажа успешно обновлён!")
            return redirect('crews_list')
    return redirect('crews_list')


@permission_required('logistics_app.delete_crew', raise_exception=True)
def delete_crew(request, crew_id):
    crew = get_object_or_404(Crew, id=crew_id)
    crew.delete()
    messages.success(request, "Член экипажа успешно удалён!")
    return redirect('crews_list')

# === PORTS ===
@permission_required('logistics_app.view_port', raise_exception=True)
def port_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле для сортировки
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    if order == 'desc':
        sort_by = f'-{sort_by}'

    ports = Port.objects.all()

    # Поиск
    if query:
        ports = ports.filter(
            Q(name__icontains=query) | 
            Q(coordinates__icontains=query)
        )

    # Сортировка
    ports = ports.order_by(sort_by)

    # Пагинация
    paginator = Paginator(ports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления порта
    if request.method == 'POST' and 'add-port' in request.POST:
        if request.user.has_perm('logistics_app.add_port'):
            port_form = PortForm(request.POST)
            if port_form.is_valid():
                port_form.save()
                messages.success(request, "Порт успешно добавлен!")
                return redirect('ports_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        port_form = PortForm()

    return render(request, 'logistics_app/ports_list.html', {
        'page_obj': page_obj,
        'port_form': port_form,
        'query': query,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
    })

# Редактирование порта
@permission_required('logistics_app.change_port', raise_exception=True)
def edit_port(request, port_id):
    port = get_object_or_404(Port, id=port_id)
    if request.method == 'POST':
        form = PortForm(request.POST, instance=port)
        if form.is_valid():
            form.save()
            messages.success(request, 'Порт успешно обновлён!')
    return redirect('ports_list')

# Удаление порта
@permission_required('logistics_app.delete_port', raise_exception=True)
def delete_port(request, port_id):
    port = get_object_or_404(Port, id=port_id)
    try:
        port.delete()
        messages.success(request, f'Порт "{port.name}" успешно удалён.')
    except Exception as e:
        messages.error(request, f'Ошибка удаления порта: {e}')
    return redirect('ports_list')


# === SERVICES ===
@permission_required('logistics_app.view_service', raise_exception=True)
def service_list(request):
    sort_by = request.GET.get('sort', 'ship')  # Сортировка по умолчанию
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    services = Service.objects.select_related('ship', 'crew_employee')
    if query:
        services = services.filter(
            Q(ship__name__icontains=query) |
            Q(crew_employee__last_name__icontains=query)
        )
    services = services.order_by(sort_by)

    ships = Ship.objects.all()
    crew_employees = Crew.objects.filter(post='Сотрудник')
    # Пагинация
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления обслуживания
    if request.method == 'POST' and 'add-service' in request.POST:
        if request.user.has_perm('logistics_app.add_service'):
            form = ServiceForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Запись обслуживания успешно добавлена!")
                return redirect('services_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = ServiceForm()

    return render(request, 'logistics_app/services_list.html', {
        'page_obj': page_obj,
        'services': services,
        'form': form,
        'current_sort': request.GET.get('sort', 'ship'),
        'current_order': order,
        'query': query,
        'ships': ships,
        'crew_employees': crew_employees,
    })


@permission_required('logistics_app.change_service', raise_exception=True)
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись обслуживания успешно обновлена!")
            return redirect('services_list')
    return redirect('services_list')


@permission_required('logistics_app.delete_service', raise_exception=True)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, "Запись обслуживания успешно удалена!")
    return redirect('services_list')

# === SHIPTYPES ===
@permission_required('logistics_app.view_shiptype', raise_exception=True)
def shiptype_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')    # Порядок сортировки по умолчанию
    query = request.GET.get('q', '')           # Поисковый запрос

    # Обработка порядка сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    shiptypes = Shiptype.objects.all()
    if query:
        shiptypes = shiptypes.filter(Q(name__icontains=query))
    shiptypes = shiptypes.order_by(sort_by)

    # Пагинация
    paginator = Paginator(shiptypes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Обработка добавления нового типа судна
    if request.method == 'POST' and 'add-shiptype' in request.POST:
        if request.user.has_perm('logistics_app.add_shiptype'):
            form = ShipTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Тип судна успешно добавлен!")
                return redirect('shiptypes_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = ShipTypeForm()

    return render(request, 'logistics_app/shiptypes_list.html', {
        'page_obj': page_obj,
        'shiptypes': shiptypes,
        'form': form,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_shiptype', raise_exception=True)
def edit_shiptype(request, shiptype_id):
    shiptype = get_object_or_404(Shiptype, id=shiptype_id)
    if request.method == 'POST':
        form = ShipTypeForm(request.POST, instance=shiptype)
        if form.is_valid():
            form.save()
            messages.success(request, "Тип судна успешно обновлен!")
            return redirect('shiptypes_list')
    return redirect('shiptypes_list')


@permission_required('logistics_app.delete_shiptype', raise_exception=True)
def delete_shiptype(request, shiptype_id):
    shiptype = get_object_or_404(Shiptype, id=shiptype_id)
    shiptype.delete()
    messages.success(request, "Тип судна успешно удален!")
    return redirect('shiptypes_list')


# === STATUSES ===
@permission_required('logistics_app.view_status', raise_exception=True)
def status_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    statuses = Status.objects.all()
    if query:
        statuses = statuses.filter(Q(name__icontains=query))
    statuses = statuses.order_by(sort_by)

    # Пагинация
    paginator = Paginator(statuses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления статуса
    if request.method == 'POST' and 'add-status' in request.POST:
        if request.user.has_perm('logistics_app.add_status'):
            form = StatusForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Статус успешно добавлен!")
                return redirect('statuses_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = StatusForm()

    return render(request, 'logistics_app/statuses_list.html', {
        'page_obj': page_obj,
        'statuses': statuses,
        'form': form,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_status', raise_exception=True)
def edit_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно обновлён!")
            return redirect('statuses_list')
    return redirect('statuses_list')


@permission_required('logistics_app.delete_status', raise_exception=True)
def delete_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    status.delete()
    messages.success(request, "Статус успешно удалён!")
    return redirect('statuses_list')

# === STREETS ===
@permission_required('logistics_app.view_street', raise_exception=True)
def street_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле для сортировки
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    if order == 'desc':
        sort_by = f'-{sort_by}'

    streets = Street.objects.all()

    # Поиск
    if query:
        streets = streets.filter(name__icontains=query)

    # Сортировка
    streets = streets.order_by(sort_by)

    # Пагинация
    paginator = Paginator(streets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Добавление улицы
    if request.method == 'POST' and 'add-street' in request.POST:
        if request.user.has_perm('logistics_app.add_street'):
            street_form = StreetForm(request.POST)
            if street_form.is_valid():
                street_form.save()
                messages.success(request, "Улица успешно добавлена!")
                return redirect('streets_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        street_form = StreetForm()

    return render(request, 'logistics_app/streets_list.html', {
        'page_obj': page_obj,
        'street_form': street_form,
        'query': query,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
    })

# Редактирование улицы
@permission_required('logistics_app.change_street', raise_exception=True)
def edit_street(request, street_id):
    street = get_object_or_404(Street, id=street_id)
    if request.method == 'POST':
        form = StreetForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            messages.success(request, 'Улица успешно обновлена!')
    return redirect('streets_list')

# Удаление улицы
@permission_required('logistics_app.delete_street', raise_exception=True)
def delete_street(request, street_id):
    street = get_object_or_404(Street, id=street_id)
    try:
        street.delete()
        messages.success(request, f'Улица "{street.name}" успешно удалена.')
    except Exception as e:
        messages.error(request, f'Ошибка удаления улицы: {e}')
    return redirect('streets_list')

# === CARGOBATCHES ===
@permission_required('logistics_app.view_cargobatch', raise_exception=True)
def cargobatch_list(request):
    sort_by = request.GET.get('sort', 'number_declaration')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')                  # Порядок сортировки
    query = request.GET.get('q', '')                         # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    cargo_batches = Cargobatch.objects.select_related(
        'ship', 'port_of_departure', 'port_of_arrival', 'client_recipient', 'client_sender'
    )
    if query:
        cargo_batches = cargo_batches.filter(
            Q(customs_number__icontains=query) |
            Q(number_declaration__icontains=query) |
            Q(departure_date__icontains=query) |
            Q(arrival_date__icontains=query) |
            Q(ship__name__icontains=query) |
            Q(port_of_departure__name__icontains=query) |
            Q(port_of_arrival__name__icontains=query) |
            Q(client_recipient__name__icontains=query) |
            Q(client_sender__name__icontains=query) 
        )
    cargo_batches = cargo_batches.order_by(sort_by)

    # Пагинация
    paginator = Paginator(cargo_batches, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления партии груза
    if request.method == 'POST' and 'add-cargo-batch' in request.POST:
        if request.user.has_perm('logistics_app.add_cargobatch'):
            form = CargoBatchForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Партия груза успешно добавлена!")
                return redirect('cargobatches_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = CargoBatchForm()

    # Данные для выпадающих списков
    ships = Ship.objects.all()
    ports = Port.objects.all()
    clients = Client.objects.all()

    return render(request, 'logistics_app/cargobatches_list.html', {
        'page_obj': page_obj,
        'cargo_batches': cargo_batches,
        'form': form,
        'ships': ships,
        'ports': ports,
        'clients': clients,
        'current_sort': request.GET.get('sort', 'number_declaration'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_cargobatch', raise_exception=True)
def edit_cargobatch(request, cargobatch_id):
    cargo_batch = get_object_or_404(Cargobatch, id=cargobatch_id)
    if request.method == 'POST':
        form = CargoBatchForm(request.POST, instance=cargo_batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Партия груза успешно обновлена!")
            return redirect('cargobatches_list')
    return redirect('cargobatches_list')


@permission_required('logistics_app.delete_cargobatch', raise_exception=True)
def delete_cargobatch(request, cargobatch_id):
    cargo_batch = get_object_or_404(Cargobatch, id=cargobatch_id)
    cargo_batch.delete()
    messages.success(request, "Партия груза успешно удалена!")
    return redirect('cargobatches_list')

# === UNITOFMEASUREMENTS ===
@permission_required('logistics_app.view_unitofmeasurement', raise_exception=True)
def unitofmeasurement_list(request):
    sort_by = request.GET.get('sort', 'name')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    units = Unitofmeasurement.objects.all()
    if query:
        units = units.filter(Q(name__icontains=query))
    units = units.order_by(sort_by)

    # Пагинация
    paginator = Paginator(units, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления единицы измерения
    if request.method == 'POST' and 'add-unit' in request.POST:
        if request.user.has_perm('logistics_app.add_unitofmeasurement'):
            form = UnitOfMeasurementForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Единица измерения успешно добавлена!")
                return redirect('unitofmeasurements_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = UnitOfMeasurementForm()

    return render(request, 'logistics_app/unitofmeasurements_list.html', {
        'page_obj': page_obj,
        'units': units,
        'form': form,
        'current_sort': request.GET.get('sort', 'name'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_unitofmeasurement', raise_exception=True)
def edit_unitofmeasurement(request, unit_id):
    unit = get_object_or_404(Unitofmeasurement, id=unit_id)
    if request.method == 'POST':
        form = UnitOfMeasurementForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, "Единица измерения успешно обновлена!")
            return redirect('unitofmeasurements_list')
    return redirect('unitofmeasurements_list')


@permission_required('logistics_app.delete_unitofmeasurement', raise_exception=True)
def delete_unitofmeasurement(request, unit_id):
    unit = get_object_or_404(Unitofmeasurement, id=unit_id)
    unit.delete()
    messages.success(request, "Единица измерения успешно удалена!")
    return redirect('unitofmeasurements_list')

# === SUMMARIES ===
@permission_required('logistics_app.view_summary', raise_exception=True)
def summary_list(request):
    sort_by = request.GET.get('sort', 'cargo_batch')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')           # Порядок сортировки
    query = request.GET.get('q', '')                  # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    summaries = Summary.objects.select_related('cargo_batch', 'cargo')
    if query:
        summaries = summaries.filter(
            Q(cargo_batch__customs_number__icontains=query) |
            Q(cargo__name__icontains=query)
        )
    summaries = summaries.order_by(sort_by)

    # Пагинация
    paginator = Paginator(summaries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления сводки
    if request.method == 'POST' and 'add-summary' in request.POST:
        if request.user.has_perm('logistics_app.add_summary'):
            form = SummaryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Сводка успешно добавлена!")
                return redirect('summaries_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = SummaryForm()

    # Передача данных в шаблон
    cargo_batches = Cargobatch.objects.all()
    cargos = Cargo.objects.all()

    return render(request, 'logistics_app/summaries_list.html', {
        'page_obj': page_obj,
        'summaries': summaries,
        'form': form,
        'cargo_batches': cargo_batches,
        'cargos': cargos,
        'current_sort': request.GET.get('sort', 'cargo_batch'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_summary', raise_exception=True)
def edit_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    if request.method == 'POST':
        form = SummaryForm(request.POST, instance=summary)
        if form.is_valid():
            form.save()
            messages.success(request, "Сводка успешно обновлена!")
            return redirect('summaries_list')
    return redirect('summaries_list')


@permission_required('logistics_app.delete_summary', raise_exception=True)
def delete_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    summary.delete()
    messages.success(request, "Сводка успешно удалена!")
    return redirect('summaries_list')

# === TRANSPORTATIONS ===
@permission_required('logistics_app.view_transportation', raise_exception=True)
def transportation_list(request):
    sort_by = request.GET.get('sort', 'ship')  # Поле сортировки по умолчанию
    order = request.GET.get('order', 'asc')    # Порядок сортировки
    query = request.GET.get('q', '')           # Поисковый запрос

    # Обработка направления сортировки
    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Фильтрация и сортировка
    transportations = Transportation.objects.select_related('ship', 'route')
    if query:
        transportations = transportations.filter(
            Q(ship__name__icontains=query) |
            Q(route__departure_date__icontains=query)
        )
    transportations = transportations.order_by(sort_by)

    # Пагинация
    paginator = Paginator(transportations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форма для добавления перевозки
    if request.method == 'POST' and 'add-transportation' in request.POST:
        if request.user.has_perm('logistics_app.add_transportation'):
            form = TransportationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Перевозка успешно добавлена!")
                return redirect('transportations_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        form = TransportationForm()

    # Данные для выпадающих списков
    ships = Ship.objects.all()
    routes = Route.objects.all()

    return render(request, 'logistics_app/transportations_list.html', {
        'page_obj': page_obj,
        'transportations': transportations,
        'form': form,
        'ships': ships,
        'routes': routes,
        'current_sort': request.GET.get('sort', 'ship'),
        'current_order': order,
        'query': query,
    })


@permission_required('logistics_app.change_transportation', raise_exception=True)
def edit_transportation(request, transportation_id):
    transportation = get_object_or_404(Transportation, id=transportation_id)
    if request.method == 'POST':
        form = TransportationForm(request.POST, instance=transportation)
        if form.is_valid():
            form.save()
            messages.success(request, "Перевозка успешно обновлена!")
            return redirect('transportations_list')
    return redirect('transportations_list')


@permission_required('logistics_app.delete_transportation', raise_exception=True)
def delete_transportation(request, transportation_id):
    transportation = get_object_or_404(Transportation, id=transportation_id)
    transportation.delete()
    messages.success(request, "Перевозка успешно удалена!")
    return redirect('transportations_list')