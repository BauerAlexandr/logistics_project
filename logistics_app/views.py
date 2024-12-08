from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from .models import Client, Ship, Cargo, Route, Pier, Bank, City, Crew, Port, Service, Shiptype
from .models import Status, Street, Cargobatch, Unitofmeasurement, Summary, Transportation
from .forms import UserRegistrationForm, UserLoginForm, ClientForm, ShipForm, CargoForm, RouteForm, PierForm
from .forms import BankForm, CargoBatchForm, CityForm, CrewForm, PortForm, ServiceForm, ShipTypeForm
from .forms import StatusForm, StreetForm, SummaryForm, TransportationForm, UnitOfMeasurementForm


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

# === PIERS ===
@permission_required('logistics_app.view_pier', raise_exception=True)
def pier_list(request):
    piers = Pier.objects.select_related('route', 'port').all()

    # Обработка добавления нового пирса
    if request.method == 'POST' and 'add-pier' in request.POST:
        if request.user.has_perm('logistics_app.add_pier'):
            pier_form = PierForm(request.POST)
            if pier_form.is_valid():
                pier_form.save()
                return redirect('piers_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        pier_form = PierForm()

    return render(request, 'logistics_app/piers_list.html', {
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
            return redirect('piers_list')
    else:
        form = PierForm(instance=pier)
    
    return redirect('piers_list')

# === BANK ===
@permission_required('logistics_app.view_bank', raise_exception=True)
def bank_list(request):
    banks = Bank.objects.all()

    if request.method == 'POST' and 'add-bank' in request.POST:
        if request.user.has_perm('logistics_app.add_bank'):
            bank_form = BankForm(request.POST)
            if bank_form.is_valid():
                bank_form.save()
                return redirect('banks_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        bank_form = BankForm()

    return render(request, 'logistics_app/banks_list.html', {
        'banks': banks,
        'bank_form': bank_form,
    })


@permission_required('logistics_app.change_bank', raise_exception=True)
def edit_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)

    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            return redirect('banks_list')
    else:
        form = BankForm(instance=bank)

    return redirect('banks_list')

# === CITIES ===
@permission_required('logistics_app.view_city', raise_exception=True)
def city_list(request):
    cities = City.objects.all()

    if request.method == 'POST' and 'add-city' in request.POST:
        if request.user.has_perm('logistics_app.add_city'):
            city_form = CityForm(request.POST)
            if city_form.is_valid():
                city_form.save()
                return redirect('cities_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        city_form = CityForm()

    return render(request, 'logistics_app/cities_list.html', {
        'cities': cities,
        'city_form': city_form,
    })


@permission_required('logistics_app.change_city', raise_exception=True)
def edit_city(request, city_id):
    city = get_object_or_404(City, id=city_id)

    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('cities_list')
    else:
        form = CityForm(instance=city)

    return redirect('cities_list')


# === CREWS ===
@permission_required('logistics_app.view_crew', raise_exception=True)
def crew_list(request):
    crews = Crew.objects.all()

    if request.method == 'POST' and 'add-crew' in request.POST:
        if request.user.has_perm('logistics_app.add_crew'):
            crew_form = CrewForm(request.POST)
            if crew_form.is_valid():
                crew_form.save()
                return redirect('crews_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        crew_form = CrewForm()

    return render(request, 'logistics_app/crews_list.html', {
        'crews': crews,
        'crew_form': crew_form,
    })


@permission_required('logistics_app.change_crew', raise_exception=True)
def edit_crew(request, crew_id):
    crew = get_object_or_404(Crew, id=crew_id)

    if request.method == 'POST':
        form = CrewForm(request.POST, instance=crew)
        if form.is_valid():
            form.save()
            return redirect('crews_list')
    else:
        form = CrewForm(instance=crew)

    return redirect('crews_list')


# === PORTS ===
@permission_required('logistics_app.view_port', raise_exception=True)
def port_list(request):
    ports = Port.objects.all()

    if request.method == 'POST' and 'add-port' in request.POST:
        if request.user.has_perm('logistics_app.add_port'):
            port_form = PortForm(request.POST)
            if port_form.is_valid():
                port_form.save()
                return redirect('ports_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        port_form = PortForm()

    return render(request, 'logistics_app/ports_list.html', {
        'ports': ports,
        'port_form': port_form,
    })


@permission_required('logistics_app.change_port', raise_exception=True)
def edit_port(request, port_id):
    port = get_object_or_404(Port, id=port_id)

    if request.method == 'POST':
        form = PortForm(request.POST, instance=port)
        if form.is_valid():
            form.save()
            return redirect('ports_list')
    else:
        form = PortForm(instance=port)

    return redirect('ports_list')


# === SERVICES ===
@permission_required('logistics_app.view_service', raise_exception=True)
def service_list(request):
    services = Service.objects.select_related('ship', 'crew_employee').all()

    # Обработка добавления нового пирса
    if request.method == 'POST' and 'add-service' in request.POST:
        if request.user.has_perm('logistics_app.add_service'):
            service_form = ServiceForm(request.POST)
            if service_form.is_valid():
                service_form.save()
                return redirect('services_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        service_form = ServiceForm()

    return render(request, 'logistics_app/services_list.html', {
        'services': services,
        'service_form': service_form,
    })

@permission_required('logistics_app.change_service', raise_exception=True)
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm(instance=service)
    
    return redirect('services_list')

# === SHIPTYPES ===
@permission_required('logistics_app.view_shiptype', raise_exception=True)
def shiptype_list(request):
    shiptypes = Shiptype.objects.all()

    # Обработка добавления нового пирса
    if request.method == 'POST' and 'add-shiptype' in request.POST:
        if request.user.has_perm('logistics_app.add_shiptype'):
            shiptype_form = ShipTypeForm(request.POST)
            if shiptype_form.is_valid():
                shiptype_form.save()
                return redirect('shiptypes_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        shiptype_form = ShipTypeForm()

    return render(request, 'logistics_app/shiptypes_list.html', {
        'shiptypes': shiptypes,
        'shiptype_form': shiptype_form,
    })

@permission_required('logistics_app.change_shiptype', raise_exception=True)
def edit_shiptype(request, shiptype_id):
    shiptype = get_object_or_404(Shiptype, id=shiptype_id)
    
    if request.method == 'POST':
        form = ShipTypeForm(request.POST, instance=shiptype)
        if form.is_valid():
            form.save()
            return redirect('shiptypes_list')
    else:
        form = ShipTypeForm(instance=shiptype)
    
    return redirect('shiptypes_list')

# === STATUSES ===
@permission_required('logistics_app.view_status', raise_exception=True)
def status_list(request):
    statuses = Status.objects.all()

    if request.method == 'POST' and 'add-status' in request.POST:
        if request.user.has_perm('logistics_app.add_status'):
            status_form = StatusForm(request.POST)
            if status_form.is_valid():
                status_form.save()
                return redirect('statuses_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        status_form = StatusForm()

    return render(request, 'logistics_app/statuses_list.html', {
        'statuses': statuses,
        'status_form': status_form,
    })


@permission_required('logistics_app.change_status', raise_exception=True)
def edit_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('statuses_list')
    else:
        form = StatusForm(instance=status)

    return redirect('statuses_list')

# === STREETS ===
@permission_required('logistics_app.view_street', raise_exception=True)
def street_list(request):
    streets = Street.objects.all()

    if request.method == 'POST' and 'add-street' in request.POST:
        if request.user.has_perm('logistics_app.add_street'):
            street_form = StreetForm(request.POST)
            if street_form.is_valid():
                street_form.save()
                return redirect('streets_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        street_form = StreetForm()

    return render(request, 'logistics_app/streets_list.html', {
        'streets': streets,
        'street_form': street_form,
    })


@permission_required('logistics_app.change_street', raise_exception=True)
def edit_street(request, street_id):
    street = get_object_or_404(Street, id=street_id)

    if request.method == 'POST':
        form = StreetForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            return redirect('streets_list')
    else:
        form = StreetForm(instance=street)

    return redirect('streets_list')

# === CARGOBATCHES ===
@permission_required('logistics_app.view_cargobatch', raise_exception=True)
def cargobatch_list(request):
    cargobatches = Cargobatch.objects.all()

    if request.method == 'POST' and 'add-cargobatch' in request.POST:
        if request.user.has_perm('logistics_app.add_cargobatch'):
            cargobatch_form = CargoBatchForm(request.POST)
            if cargobatch_form.is_valid():
                cargobatch_form.save()
                return redirect('cargobatches_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        cargobatch_form = CargoBatchForm()

    return render(request, 'logistics_app/cargobatches_list.html', {
        'cargobatches': cargobatches,
        'cargobatch_form': cargobatch_form,
    })


@permission_required('logistics_app.change_cargobatch', raise_exception=True)
def edit_cargobatch(request, cargobatch_id):
    cargobatch = get_object_or_404(Cargobatch, id=cargobatch_id)

    if request.method == 'POST':
        form = CargoBatchForm(request.POST, instance=cargobatch)
        if form.is_valid():
            form.save()
            return redirect('cargobatches_list')
    else:
        form = CargoBatchForm(instance=cargobatch)

    return redirect('cargobatches_list')

# === UNITOFMEASUREMENTS ===
@permission_required('logistics_app.view_unitofmeasurement', raise_exception=True)
def unitofmeasurement_list(request):
    unitofmeasurements = Unitofmeasurement.objects.all()

    if request.method == 'POST' and 'add-unitofmeasurement' in request.POST:
        if request.user.has_perm('logistics_app.add_unitofmeasurement'):
            unitofmeasurement_form = UnitOfMeasurementForm(request.POST)
            if unitofmeasurement_form.is_valid():
                unitofmeasurement_form.save()
                return redirect('unitofmeasurements_list')
        else:
            return render(request, 'logistics_app/403.html', status=403)
    else:
        unitofmeasurement_form = UnitOfMeasurementForm()

    return render(request, 'logistics_app/unitofmeasurements_list.html', {
        'unitofmeasurements': unitofmeasurements,
        'unitofmeasurement_form': unitofmeasurement_form,
    })


@permission_required('logistics_app.change_unitofmeasurement', raise_exception=True)
def edit_unitofmeasurement(request, unitofmeasurement_id):
    unitofmeasurement = get_object_or_404(Unitofmeasurement, id=unitofmeasurement_id)

    if request.method == 'POST':
        form = UnitOfMeasurementForm(request.POST, instance=unitofmeasurement)
        if form.is_valid():
            form.save()
            return redirect('unitofmeasurements_list')
    else:
        form = UnitOfMeasurementForm(instance=unitofmeasurement)

    return redirect('unitofmeasurements_list')

# === SUMMARIES ===
@permission_required('logistics_app.view_summary', raise_exception=True)
def summary_list(request):
    summaries = Summary.objects.select_related('cargo_batch', 'cargo').all()

    # Обработка добавления нового пирса
    if request.method == 'POST' and 'add-summary' in request.POST:
        if request.user.has_perm('logistics_app.add_summary'):
            summary_form = SummaryForm(request.POST)
            if summary_form.is_valid():
                summary_form.save()
                return redirect('summaries_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        summary_form = SummaryForm()

    return render(request, 'logistics_app/summaries_list.html', {
        'summaries': summaries,
        'summary_form': summary_form,
    })

@permission_required('logistics_app.change_summary', raise_exception=True)
def edit_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    
    if request.method == 'POST':
        form = SummaryForm(request.POST, instance=summary)
        if form.is_valid():
            form.save()
            return redirect('summaries_list')
    else:
        form = SummaryForm(instance=summary)
    
    return redirect('summaries_list')

# === TRANSPORTATIONS ===
@permission_required('logistics_app.view_transportation', raise_exception=True)
def transportation_list(request):
    transportations = Transportation.objects.select_related('ship', 'route').all()

    # Обработка добавления нового пирса
    if request.method == 'POST' and 'add-transportation' in request.POST:
        if request.user.has_perm('logistics_app.add_transportation'):
            transportation_form = TransportationForm(request.POST)
            if transportation_form.is_valid():
                transportation_form.save()
                return redirect('transportations_list')
        else:
            # Если нет разрешения, показываем ошибку
            return render(request, 'logistics_app/403.html', status=403)
    else:
        transportation_form = TransportationForm()

    return render(request, 'logistics_app/transportations_list.html', {
        'transportations': transportations,
        'transportation_form': transportation_form,
    })

@permission_required('logistics_app.change_transportation', raise_exception=True)
def edit_transportation(request, transportation_id):
    transportation = get_object_or_404(Transportation, id=transportation_id)
    
    if request.method == 'POST':
        form = TransportationForm(request.POST, instance=transportation)
        if form.is_valid():
            form.save()
            return redirect('transportations_list')
    else:
        form = TransportationForm(instance=transportation)
    
    return redirect('transportations_list')