from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from .models import Client, Ship, Cargo, Route, Pier
from .forms import UserRegistrationForm, UserLoginForm, ClientForm, ShipForm, CargoForm, RouteForm, PierForm


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
def ships_list(request):
    ships = Ship.objects.select_related('home_port', 'ship_type').all()

    if request.method == 'POST' and 'add-ship' in request.POST:
        if request.user.has_perm('logistics_app.add_ship'):
            ship_form = ShipForm(request.POST)
            if ship_form.is_valid():
                ship_form.save()
                return redirect('ships_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        ship_form = ShipForm()

    return render(request, 'logistics_app/ships_list.html', {
        'ships': ships,
        'ship_form': ship_form,
    })


@permission_required('logistics_app.change_ship', raise_exception=True)
def edit_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    
    if request.method == 'POST':
        edit_ship_form = ShipForm(request.POST, instance=ship)
        if edit_ship_form.is_valid():
            edit_ship_form.save()
            return redirect('ships_list')
    else:
        edit_ship_form = ShipForm(instance=ship)
    
    return redirect('ships_list')





# === CARGO ===
@permission_required('logistics_app.view_cargo', raise_exception=True)
def cargo_list(request):
    cargos = Cargo.objects.select_related('unit_of_measurement').all()

    if request.method == 'POST' and 'add-cargo' in request.POST:
        if request.user.has_perm('logistics_app.add_cargo'):
            cargo_form = CargoForm(request.POST)
            if cargo_form.is_valid():
                cargo_form.save()
                return redirect('cargo_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        cargo_form = CargoForm()

    return render(request, 'logistics_app/cargo_list.html', {
        'cargos': cargos,
        'cargo_form': cargo_form,
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


# === CLIENTS ===
@permission_required('logistics_app.view_client', raise_exception=True)
def clients_list(request):
    clients = Client.objects.all()
    
    if request.method == 'POST' and 'add-client' in request.POST:
        if request.user.has_perm('logistics_app.add_client'):
            client_form = ClientForm(request.POST)
            if client_form.is_valid():
                client_form.save()
                return redirect('clients_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        client_form = ClientForm()

    return render(request, 'logistics_app/clients_list.html', {
        'clients': clients,
        'client_form': client_form,
    })


@permission_required('logistics_app.change_client', raise_exception=True)
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    
    return redirect('clients_list')

# === ROUTES ===
@permission_required('logistics_app.view_route', raise_exception=True)
def routes_list(request):
    routes = Route.objects.all()

    if request.method == 'POST' and 'add-route' in request.POST:
        if request.user.has_perm('logistics_app.add_route'):
            route_form = RouteForm(request.POST)
            if route_form.is_valid():
                route_form.save()
                return redirect('routes_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        route_form = RouteForm()

    return render(request, 'logistics_app/routes_list.html', {
        'routes': routes,
        'route_form': route_form,
    })


@permission_required('logistics_app.change_route', raise_exception=True)
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('routes_list')
    else:
        form = RouteForm(instance=route)
    
    return redirect('routes_list')

# === REPORTS ===
def reports(request):
    return render(request, 'logistics_app/reports.html')

# Добавление пирса
@permission_required('logistics_app.view_pier', raise_exception=True)
def pier_list(request):
    piers = Pier.objects.select_related('route', 'port').all()

    # Обработка добавления нового пирса
    if request.method == 'POST' and 'add-pier' in request.POST:
        if request.user.has_perm('logistics_app.add_pier'):
            pier_form = PierForm(request.POST)
            if pier_form.is_valid():
                pier_form.save()
                return redirect('pier_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        pier_form = PierForm()

    return render(request, 'logistics_app/pier_list.html', {
        'piers': piers,
        'pier_form': pier_form,
    })

@permission_required('logistics_app.change_pier', raise_exception=True)
def edit_pier(request, pier_id):
    pier = get_object_or_404(Pier, id=pier_id)
    
    if request.method == 'POST':
        form = PierForm(request.POST, instance=pier)
        if form.is_valid():
            form.save()
            return redirect('pier_list')
    else:
        form = PierForm(instance=pier)
    
    return redirect('pier_list')