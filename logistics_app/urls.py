from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница

    # Страницы для кораблей
    path('ships/', views.ships_list, name='ships_list'),
    path('edit-ship/<int:ship_id>/', views.edit_ship, name='edit_ship'),
    path('add-ship/', views.ships_list, name='add_ship'),
    path('ships/<int:ship_id>/', views.ship_detail, name='ship_detail'),

    # Страницы для грузов
    path('cargos/', views.cargo_list, name='cargo_list'),
    path('edit-cargo/<int:cargo_id>/', views.edit_cargo, name='edit_cargo'),
    path('add-cargo/', views.cargo_list, name='add_cargo'),
    path('cargo/<int:cargo_id>/', views.cargo_detail, name='cargo_detail'),

    # Страницы для клиентов
    path('clients/', views.clients_list, name='clients_list'),
    path('edit-client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('add-client/', views.clients_list, name='add_client'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),

    # Страницы для маршрутов
    path('routes/', views.routes_list, name='routes_list'),
    path('edit-route/<int:route_id>/', views.edit_route, name='edit_route'),
    path('add-route/', views.routes_list, name='add_route'),
    path('routes/<int:route_id>/', views.route_detail, name='route_detail'),

    # Отчёты
    path('reports/', views.reports, name='reports'),

    
    path('add-pier/', views.add_pier, name='add_pier'),
]