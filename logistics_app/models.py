# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    ],
        default='client',
        verbose_name='Role'
    )

    def is_director(self):
        return self.role == 'director'

    def is_manager(self):
        return self.role == 'manager'

    def is_client(self):
        return self.role == 'client'

    def __str__(self):
        return f"{self.username} ({self.role})"


class Bank(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bank'

    def __str__(self):
        return self.name
 

class Cargo(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    declared_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    unit_of_measurement = models.ForeignKey('Unitofmeasurement', models.DO_NOTHING, blank=True, null=True)
    insured_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargo'

    def __str__(self):
        return self.name


class Cargobatch(models.Model):
    number_declaration = models.CharField(max_length=23, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    ship = models.ForeignKey('Ship', models.DO_NOTHING, blank=True, null=True)
    port_of_departure = models.ForeignKey('Port', models.DO_NOTHING, blank=True, null=True)
    port_of_arrival = models.ForeignKey('Port', models.DO_NOTHING, related_name='cargobatch_port_of_arrival_set', blank=True, null=True)
    client_recipient = models.ForeignKey('Client', models.DO_NOTHING, blank=True, null=True)
    client_sender = models.ForeignKey('Client', models.DO_NOTHING, related_name='cargobatch_client_sender_set', blank=True, null=True)
    customs_number = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargobatch'

    def __str__(self):
        return self.customs_number or "Без номера"


class City(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'city'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50)
    tax_id_number = models.CharField(max_length=12, blank=True, null=True)
    client_account = models.CharField(unique=True, max_length=20, blank=True, null=True)
    street = models.ForeignKey('Street', models.DO_NOTHING, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)
    bank = models.ForeignKey(Bank, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'

    def __str__(self):
        return self.name


class Crew(models.Model):
    POST_CHOICES = [
        ('Капитан', 'Капитан'),
        ('Сотрудник', 'Сотрудник'),
        
    ]
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    post = models.CharField(max_length=20, choices=POST_CHOICES)

    class Meta:
        managed = False
        db_table = 'crew'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Pier(models.Model):
    PURPOSE_CHOICES = [
        ('Порт прибытия', 'Порт прибытия'),
        ('Порт отправления', 'Порт отправления'),
        ('Промежуточный порт', 'Промежуточный порт'),
    ]
    route = models.ForeignKey('Route', models.DO_NOTHING, blank=True, null=True)
    port = models.ForeignKey('Port', models.DO_NOTHING, blank=True, null=True)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)

    class Meta:
        managed = False
        db_table = 'pier'

    def __str__(self):
        return f"{self.port} - {self.purpose}"


class Port(models.Model):
    name = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'port'

    def __str__(self):
        return self.name


class Route(models.Model):
    departure_date = models.DateField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route'

    def __str__(self):
        return f"{self.departure_date} - {self.arrival_date}"


class Service(models.Model):
    ship = models.ForeignKey('Ship', models.DO_NOTHING, blank=True, null=True)
    crew_employee = models.ForeignKey(Crew, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service'

    def __str__(self):
        return f"Service for {self.ship}"


class Ship(models.Model):
    registration_number = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    capacity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)
    photo = models.CharField(max_length=50, blank=True, null=True)
    home_port = models.ForeignKey(Port, models.DO_NOTHING, blank=True, null=True)
    ship_type = models.ForeignKey('Shiptype', models.DO_NOTHING, blank=True, null=True)
    crew_captain = models.ForeignKey(Crew, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ship'

    def __str__(self):
        return self.name


class Shiptype(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shiptype'

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status'

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'street'

    def __str__(self):
        return self.name


class Summary(models.Model):
    cargo_batch = models.ForeignKey(Cargobatch, models.DO_NOTHING, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'summary'

    def __str__(self):
        return f"Summary for {self.cargo_batch}"


class Transportation(models.Model):
    ship = models.ForeignKey(Ship, models.DO_NOTHING, blank=True, null=True)
    route = models.ForeignKey(Route, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transportation'

    def __str__(self):
        return f"Transportation on {self.ship}"


class Unitofmeasurement(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'unitofmeasurement'

    def __str__(self):
        return self.name
