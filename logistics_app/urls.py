from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/director/', views.director_dashboard, name='director_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    
    path('debug/', views.debug_view, name='debug'),

    path('', views.index, name='index'),  # Главная страница

    # Страницы для кораблей
    path('ships/', views.ships_list, name='ships_list'),
    path('edit-ship/<int:ship_id>/', views.edit_ship, name='edit_ship'),
    path('add-ship/', views.ships_list, name='add_ship'),

    # Страницы для грузов
    path('cargos/', views.cargo_list, name='cargo_list'),
    path('edit-cargo/<int:cargo_id>/', views.edit_cargo, name='edit_cargo'),
    path('add-cargo/', views.cargo_list, name='add_cargo'),

    # Страницы для клиентов
    path('clients/', views.clients_list, name='clients_list'),
    path('edit-client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('add-client/', views.clients_list, name='add_client'),

    # Страницы для маршрутов
    path('routes/', views.routes_list, name='routes_list'),
    path('edit-route/<int:route_id>/', views.edit_route, name='edit_route'),
    path('add-route/', views.routes_list, name='add_route'),

    # Отчёты
    path('reports/', views.reports, name='reports'),

    
    path('piers/', views.pier_list, name='pier_list'),
    path('edit-pier/<int:pier_id>/', views.edit_pier, name='edit_pier'),
    path('add-pier/', views.pier_list, name='add_pier'),
]