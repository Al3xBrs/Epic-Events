from django.db import models


class Collaborater(models.Model):
    teams = [
        ("SP", "support_team"),
        ("GT", "gesture_team"),
        ("SL", "sale_team"),
    ]

    id = models.UUIDField(unique=True, primary_key=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    role = models.CharField(choices=teams, max_length=2)


class Customer(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    create_date = models.DateField()
    update_date = models.DateField()
    commercial = models.ForeignKey(
        to=Collaborater,
        on_delete=models.SET_NULL,
        null=True,
        related_name="customer_commercial",
    )


class Contract(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contract_customer",
    )
    commercial = models.ForeignKey(
        to=Collaborater,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contract_commercial",
    )
    price = models.FloatField()
    create_date = models.DateField()
    status = models.BooleanField(default=False)


class Events(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    contract = models.ForeignKey(
        to=Contract,
        on_delete=models.SET_NULL,
        null=True,
        related_name="event_contract",
    )
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="event_customer",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    support = models.ForeignKey(
        to=Collaborater,
        on_delete=models.SET_NULL,
        null=True,
        related_name="event_support",
    )
    location = models.CharField(max_length=1000)
    attendees = models.IntegerField()
    description = models.CharField(max_length=1000)
