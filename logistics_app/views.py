from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Ship, Cargo, Route, Pier
from .forms import ClientForm, ShipForm, CargoForm, RouteForm, PierForm

# Главная страница
def index(request):
    return render(request, 'logistics_app/index.html')


# === SHIPS ===
def ships_list(request):
    ships = Ship.objects.all()

    # Форма для добавления корабля
    if request.method == 'POST' and 'add-ship' in request.POST:
        ship_form = ShipForm(request.POST)
        if ship_form.is_valid():
            ship_form.save()
            return redirect('ships_list')
    else:
        ship_form = ShipForm()

    return render(request, 'logistics_app/ships_list.html', {
        'ships': ships,
        'ship_form': ship_form,
    })

def edit_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    
    if request.method == 'POST':
        form = ShipForm(request.POST, instance=ship)
        if form.is_valid():
            form.save()
            return redirect('ships_list')
    else:
        form = ShipForm(instance=ship)
    
    return redirect('ships_list')


def ship_detail(request, ship_id):
    ship = get_object_or_404(Ship, pk=ship_id)
    return render(request, 'logistics_app/ship_detail.html', {'ship': ship})


# === CARGO ===
def cargo_list(request):
    cargos = Cargo.objects.select_related('unit_of_measurement').all()

    # Обработка добавления нового груза
    if request.method == 'POST' and 'add-cargo' in request.POST:
        cargo_form = CargoForm(request.POST)
        if cargo_form.is_valid():
            cargo_form.save()
            return redirect('cargo_list')
    else:
        cargo_form = CargoForm()

    return render(request, 'logistics_app/cargo_list.html', {
        'cargos': cargos,
        'cargo_form': cargo_form,
    })


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


def cargo_detail(request, cargo_id):
    cargo = get_object_or_404(Cargo, pk=cargo_id)
    return render(request, 'logistics_app/cargo_detail.html', {'cargo': cargo})


# === CLIENTS ===
def clients_list(request):
    clients = Client.objects.all()
    
    # Форма для добавления клиента
    if request.method == 'POST' and 'add-client' in request.POST:
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client_form.save()
            return redirect('clients_list')
    else:
        client_form = ClientForm()

    return render(request, 'logistics_app/clients_list.html', {
        'clients': clients,
        'client_form': client_form,
    })

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


def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'logistics_app/client_detail.html', {'client': client})


# === ROUTES ===
def routes_list(request):
    routes = Route.objects.all()

    # Форма для добавления маршрута
    if request.method == 'POST' and 'add-route' in request.POST:
        route_form = RouteForm(request.POST)
        if route_form.is_valid():
            route_form.save()
            return redirect('routes_list')
    else:
        route_form = RouteForm()

    return render(request, 'logistics_app/routes_list.html', {
        'routes': routes,
        'route_form': route_form,
    })


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


def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'logistics_app/route_detail.html', {'route': route})


# === REPORTS ===
def reports(request):
    return render(request, 'logistics_app/reports.html')


# Добавление клиента


# Добавление корабля


# Добавление груза


# Добавление маршрута


# Добавление пирса
def add_pier(request):
    if request.method == 'POST':
        form = PierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('piers_list')
    else:
        form = PierForm()
    return render(request, 'logistics_app/add_pier.html', {'form': form})
