def menu_context(request):
    menu = [
        
        {
            "name": "Клиенты",
            
            "children": [
                {"name": "Клиенты", "url": "clients_list"},
                {"name": "Банки", "url": "banks_list"},
            ],
        },
        {
            "name": "География",
            
            "children": [
                {"name": "Города", "url": "cities_list"},
                {"name": "Улицы", "url": "streets_list"},
                {"name": "Порты", "url": "ports_list"},
                {"name": "Пирсы", "url": "piers_list"},
            ],
        },
        {
            "name": "Флотилия",
            
            "children": [
                {"name": "Корабли", "url": "ships_list"},
                {"name": "Типы судов", "url": "shiptypes_list"},
                {"name": "Обслуживание", "url": "services_list"},
                {"name": "Экипажи", "url": "crews_list"},
            ],
        },
        {
            "name": "Навигация",
            
            "children": [
                {"name": "Маршруты", "url": "routes_list"},
                {"name": "Перевозки", "url": "transportations_list"},
            ],
        },
        {
            "name": "Грузы",
            
            "children": [
                {"name": "Грузы", "url": "cargo_list"},
                {"name": "Единицы измерения", "url": "unitofmeasurements_list"},
                {"name": "Партии грузов", "url": "cargobatches_list"},
            ],
        },
        {
            "name": "Отчеты",
            
            "children": [
                {"name": "Статусы", "url": "statuses_list"},
                {"name": "Сводки", "url": "summaries_list"},
                {"name": "Документы", "url": "documents"},
            ],
        },
    ]
    return {"menu": menu}


def user_permissions(request):
    """
    Контекстный процессор для передачи разрешений пользователя в шаблоны.
    """
    if request.user.is_authenticated:
        # Получаем все разрешения пользователя
        permissions = request.user.get_all_permissions()

        # Разделяем на группы
        add_permissions = {perm.split('.')[1] for perm in permissions if perm.startswith('logistics_app.add_')}
        change_permissions = {perm.split('.')[1] for perm in permissions if perm.startswith('logistics_app.change_')}
        delete_permissions = {perm.split('.')[1] for perm in permissions if perm.startswith('logistics_app.delete_')}

        return {
            'add_permissions': add_permissions,
            'change_permissions': change_permissions,
            'delete_permissions': delete_permissions,
        }

    return {
        'add_permissions': set(),
        'change_permissions': set(),
        'delete_permissions': set(),
    }
