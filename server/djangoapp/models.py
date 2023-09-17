from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default="None")
    description = models.CharField(null=False, max_length=1000, default="None")

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"


class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"

    CAR_TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default="None")
    dealer_id = models.IntegerField(null=False, default=0)
    type = models.CharField(null=False, max_length=30, choices=CAR_TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=False, default=now)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Year: {self.year}"


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.review = review
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Dealer dealership: {self.dealership}, for car make {self.car_make} and review '{self.review}' with sentiment as {self.sentiment}"
