from django.contrib import admin
from .models import Bank, Cargo, Cargobatch, City, Client, Crew, Pier     
from .models import Port, Route, Service, Ship, Shiptype, Status, Street, Summary, Transportation, Unitofmeasurement
# Register your models here.

admin.site.register(Bank)
admin.site.register(Cargo)
admin.site.register(Cargobatch)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(Crew)
admin.site.register(Pier)
admin.site.register(Port)
admin.site.register(Route)
admin.site.register(Service)
admin.site.register(Ship)
admin.site.register(Shiptype)
admin.site.register(Status)
admin.site.register(Street)
admin.site.register(Summary)
admin.site.register(Transportation)
admin.site.register(Unitofmeasurement)
