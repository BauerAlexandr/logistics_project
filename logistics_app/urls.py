from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('documents/', views.documents, name='documents'),

    
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='logistics_app/password_reset_done.html'
    ), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('contents/', views.contents, name='contents'),
    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/director/', views.director_dashboard, name='director_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    

    path('', views.index, name='index'),

    # Страницы для кораблей
    path('ships/', views.ship_list, name='ships_list'),
    path('edit-ship/<int:ship_id>/', views.edit_ship, name='edit_ship'),
    path('add-ship/', views.ship_list, name='add_ship'),
    path('delete-ship/<int:ship_id>/', views.delete_ship, name='delete_ship'),
    path('edit-ship-photo/<int:ship_id>/', views.edit_ship_photo, name='edit_ship_photo'),

    # Страницы для грузов
    path('cargos/', views.cargo_list, name='cargo_list'),
    path('edit-cargo/<int:cargo_id>/', views.edit_cargo, name='edit_cargo'),
    path('add-cargo/', views.cargo_list, name='add_cargo'),
    path('delete-cargo/<int:cargo_id>/', views.delete_cargo, name='delete_cargo'),

    # Страницы для клиентов
    path('clients/', views.clients_list, name='clients_list'),
    path('edit-client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('add-client/', views.clients_list, name='add_client'),
    path('delete-client/<int:client_id>/', views.delete_client, name='delete_client'),


    # Страницы для маршрутов
    path('routes/', views.route_list, name='routes_list'),
    path('edit-route/<int:route_id>/', views.edit_route, name='edit_route'),
    path('add-route/', views.route_list, name='add_route'),
    path('delete-route/<int:route_id>/', views.delete_route, name='delete_route'),


    # Страницы для причалов
    path('piers/', views.pier_list, name='piers_list'),
    path('edit-pier/<int:pier_id>/', views.edit_pier, name='edit_pier'),
    path('add-pier/', views.pier_list, name='add_pier'),
    path('delete-pier/<int:pier_id>/', views.delete_pier, name='delete_pier'),

    # Страницы для банков
    path('banks/', views.bank_list, name='banks_list'),
    path('edit-bank/<int:bank_id>/', views.edit_bank, name='edit_bank'),
    path('add-bank/', views.bank_list, name='add_bank'),
    path('delete-bank/<int:bank_id>/', views.delete_bank, name='delete_bank'),

    # Страницы для партий грузов
    path('cargobatches/', views.cargobatch_list, name='cargobatches_list'),
    path('edit-cargobatch/<int:cargobatch_id>/', views.edit_cargobatch, name='edit_cargobatch'),
    path('add-cargobatch/', views.cargobatch_list, name='add_cargobatch'),
    path('delete-cargobatch/<int:cargobatch_id>/', views.delete_cargobatch, name='delete_cargobatch'),

    # Страницы для городов
    path('cities/', views.city_list, name='cities_list'),
    path('edit-city/<int:city_id>/', views.edit_city, name='edit_city'),
    path('add-city/', views.city_list, name='add_city'),
    path('delete-city/<int:city_id>/', views.delete_city, name='delete_city'),

    #Страницы для экипажа
    path('crews/', views.crew_list, name='crews_list'),
    path('edit-crew/<int:crew_id>/', views.edit_crew, name='edit_crew'),
    path('add-crew/', views.crew_list, name='add_crew'),
    path('delete-crew/<int:crew_id>/', views.delete_crew, name='delete_crew'),

    #Страницы для портов
    path('ports/', views.port_list, name='ports_list'),
    path('edit-port/<int:port_id>/', views.edit_port, name='edit_port'),
    path('add-port/', views.port_list, name='add_port'),
    path('delete-port/<int:port_id>/', views.delete_port, name='delete_port'),


    #Страницы для обслуживания
    path('services/', views.service_list, name='services_list'),
    path('edit-service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('add-service/', views.service_list, name='add_service'),
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),

    #Страницы для типов суден
    path('shiptypes/', views.shiptype_list, name='shiptypes_list'),
    path('edit-shiptype/<int:shiptype_id>/', views.edit_shiptype, name='edit_shiptype'),
    path('add-shiptype/', views.shiptype_list, name='add_shiptype'),
    path('delete-shiptype/<int:shiptype_id>/', views.delete_shiptype, name='delete_shiptype'),

    #Страницы для статусов
    path('statuses/', views.status_list, name='statuses_list'),
    path('edit-status/<int:status_id>/', views.edit_status, name='edit_status'),
    path('add-status/', views.status_list, name='add_status'),
    path('delete-status/<int:status_id>/', views.delete_status, name='delete_status'),

    #Страницы для улиц
    path('streets/', views.street_list, name='streets_list'),
    path('edit-street/<int:street_id>/', views.edit_street, name='edit_street'),
    path('add-street/', views.street_list, name='add_street'),
    path('delete-street/<int:street_id>/', views.delete_street, name='delete_street'),

    #Страницы для сводок
    path('summaries/', views.summary_list, name='summaries_list'),
    path('edit-summary/<int:summary_id>/', views.edit_summary, name='edit_summary'),
    path('add-summary/', views.summary_list, name='add_summary'),
    path('delete-summary/<int:summary_id>/', views.delete_summary, name='delete_summary'),

    #Страницы для перевозок
    path('transportations/', views.transportation_list, name='transportations_list'),
    path('edit-transportation/<int:transportation_id>/', views.edit_transportation, name='edit_transportation'),
    path('add-transportation/', views.transportation_list, name='add_transportation'),
    path('delete-transportation/<int:transportation_id>/', views.delete_transportation, name='delete_transportation'),

    #Страницы для единиц измерения
    path('unitofmeasurements/', views.unitofmeasurement_list, name='unitofmeasurements_list'),
    path('edit-unitofmeasurement/<int:unit_id>/', views.edit_unitofmeasurement, name='edit_unitofmeasurement'),
    path('add-unitofmeasurement/', views.unitofmeasurement_list, name='add_unitofmeasurement'),
    path('delete-unit/<int:unit_id>/', views.delete_unitofmeasurement, name='delete_unitofmeasurement'),
]