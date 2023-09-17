import json
import logging
import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf, post_request

logger = logging.getLogger(__name__)


def about(request):
    return render(request, "djangoapp/about.html")


def contact(request):
    return render(request, "djangoapp/contact.html")


def login_request(request):
    if request.method == "GET":
        return render(request, "djangoapp/index.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        return redirect("djangoapp:index")


def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index", context)
        else:
            context["message"] = "User already exists"
            return redirect("djangoapp:registration", context)


def get_dealerships(request):
    if request.method == "GET":
        url = "https://3e62d68d-2584-4e5c-a5ca-4d756bf80511-bluemix.cloudant.com/get-dealerships/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context = {}
        context["dealership_list"] = dealerships
        return render(request, "djangoapp/index.html", context=context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://3e62d68d-2584-4e5c-a5ca-4d756bf80511-bluemix.cloudant.com/get-reviews/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)

        if not reviews:
            return render(
                request,
                "djangoapp/dealer_details.html",
                context={
                    "dealer_id": dealer_id,
                    "reviews": [
                        {
                            "id": 1,
                            "name": "Berkly Shepley",
                            "dealership": 15,
                            "review": "Total grid-enabled service-desk",
                            "purchase": True,
                            "purchase_date": "07/11/2020",
                            "car_make": "Audi",
                            "car_model": "A6",
                            "car_year": 2010,
                            "sentiment": "positive",
                        },
                        {
                            "id": 1,
                            "name": "Gwenora Zettoi",
                            "dealership": 23,
                            "review": "Future-proofed foreground capability",
                            "purchase": True,
                            "purchase_date": "09/17/2020",
                            "car_make": "Pontiac",
                            "car_model": "Firebird",
                            "car_year": 1995,
                            "sentiment": "positive",
                        },
                        {
                            "id": 15,
                            "name": "Lisabeth Izatson",
                            "dealership": 27,
                            "review": "Upgradable neutral matrix",
                            "purchase": False,
                            "purchase_date": "12/31/2020",
                            "car_make": "BMW",
                            "car_model": "550",
                            "car_year": 2006,
                            "sentiment": "neutral",
                        },
                    ],
                },
            )

        context = {}
        context["dealer_id"] = dealer_id
        context["reviews"] = reviews
        return render(request, "djangoapp/dealer_details.html", context=context)


def add_review(request, dealer_id):
    try:
        if not request.user.is_authenticated:
            return HttpResponse("Only logged in users can post a review")

        context = {"dealer_id": dealer_id}
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars

        if request.method == "GET":
            return render(request, "djangoapp/add_review.html", context=context)

        review = {
            "dealer_id": random.randint(6, 1000),
            "time": datetime.utcnow().isoformat(),
            "dealership": dealer_id,
            "review": request.POST.get("content", ""),
            "purchase": request.POST.get("purchasecheck") == "on",
            "name": f"{request.user.first_name} {request.user.last_name}",
            "purchase_date": request.POST.get("purchasedate", ""),
        }

        carid = request.POST.get("car", "")
        if carid:
            car = CarModel.objects.get(pk=carid)
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.year

        json_payload = {"reviews": review}
        response = post_request("https://3e62d68d-2584-4e5c-a5ca-4d756bf80511-bluemix.cloudant.com/post-review/api/review", json_payload, dealerId=dealer_id)

        if "status" in response:
            print(response["status"])
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            print(response["message"])
            return HttpResponse(response["message"])

    except CarModel.DoesNotExist:
        return HttpResponse("Car not found")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
