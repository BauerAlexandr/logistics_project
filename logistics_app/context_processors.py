def menu_context(request):
    menu = [
        {"name": "Главная", "icon": "icons/house-door.svg", "url": "dashboard"},
        {
            "name": "Управление клиентами и банками",
            "icon": "icons/people.svg",
            "children": [
                {"name": "Клиенты", "url": "clients_list"},
                {"name": "Банки", "url": "banks_list"},
            ],
        },
        {
            "name": "География и логистика",
            "icon": "icons/geo-alt.svg",
            "children": [
                {"name": "Города", "url": "cities_list"},
                {"name": "Улицы", "url": "streets_list"},
                {"name": "Порты", "url": "ports_list"},
                {"name": "Пирсы", "url": "piers_list"},
            ],
        },
        {
            "name": "Флот и обслуживание",
            "icon": "icons/life-preserver.svg",
            "children": [
                {"name": "Корабли", "url": "ships_list"},
                {"name": "Типы судов", "url": "shiptypes_list"},
                {"name": "Обслуживание", "url": "services_list"},
                {"name": "Экипажи", "url": "crews_list"},
            ],
        },
        {
            "name": "Маршруты и перевозки",
            "icon": "icons/sign-merge-right.svg",
            "children": [
                {"name": "Маршруты", "url": "routes_list"},
                {"name": "Перевозки", "url": "transportations_list"},
            ],
        },
        {
            "name": "Управление грузами",
            "icon": "icons/box-seam.svg",
            "children": [
                {"name": "Грузы", "url": "cargo_list"},
                {"name": "Единицы измерения", "url": "unitofmeasurements_list"},
                {"name": "Партии грузов", "url": "cargobatches_list"},
            ],
        },
        {
            "name": "Статусы и отчёты",
            "icon": "icons/life-preserver.svg",
            "children": [
                {"name": "Статусы", "url": "statuses_list"},
                {"name": "Сводки", "url": "summaries_list"},
            ],
        },
    ]
    return {"menu": menu}
