import json
from typing import Dict, List

import requests
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview


def get_request(
    url: str,
    **kwargs,
) -> Dict:
    """
    Makes a GET request to the specified URL and returns a dictionary containing the response body.
    """
    try:
        response = requests.get(
            url,
            headers={"Content-Type": "application/json"},
            params=kwargs,
            auth=HTTPBasicAuth("apikey", kwargs["api_key"]),
        )
    except:
        local_test_dict = {
            "body": [
                {
                    "doc": {
                        "id": 0,
                        "city": "Berlin",
                        "state": "Berlin",
                        "st": "BE",
                        "address": "Wiebestr. 36/37",
                        "zip": "10553",
                        "lat": 52.530290,
                        "long": 13.319280,
                        "short_name": "Classic Remise",
                        "full_name": "Lange CI GmbH",
                    }
                },
                {
                    "doc": {
                        "id": 1,
                        "city": "El Paso",
                        "state": "Texas",
                        "st": "TX",
                        "address": "3 Nova Court",
                        "zip": "88563",
                        "lat": 31.6948,
                        "long": -106.3,
                        "short_name": "Holdlamis",
                        "full_name": "Holdlamis Car Dealership",
                    }
                },
            ]
        }
        return local_test_dict
    return json.loads(response.text)


def post_request(
    url: str,
    payload: Dict,
    **kwargs,
) -> Dict:
    """
    Makes a POST request to the specified URL and returns a dictionary containing the response body.
    """
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except:
        return {"message": "network error in POST"}
    return json.loads(response.text)


def get_dealers_from_cf(
    url: str,
    **kwargs,
) -> List:
    """
    Makes a GET request to the specified URL and returns a list of CarDealer objects.
    """
    json_result = get_request(url, **kwargs)

    results = []
    if json_result:
        for dealer in json_result["body"]:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"],
            )
            results.append(dealer_obj)
    return results


def analyze_review_sentiments(review_text: str) -> str:
    """
    Calls the Watson Natural Language Understanding API to analyze the sentiment of the given text.
    """
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/33621095-d48b-4a1d-be41-cc22d402a18d/v1/analyze"
    api_key = "qY7ok-eVR2G9r8lllGQdGnqf_Xk5bn7EOoXfcThldECO"
    version = "2022-03-30"
    feature = {"sentiment": {}}  # type: ignore

    return_analyzed_text = True
    result_json = get_request(url, api_key=api_key, text=review_text, version=version, features=feature, return_analyzed_text=return_analyzed_text)

    if "sentiment" in result_json:
        return result_json["sentiment"]["document"]["label"]
    else:
        return ""


def get_dealer_reviews_from_cf(
    url: str,
    **kwargs,
) -> List:
    """
    Makes a GET request to the specified URL and returns a list of DealerReview objects.
    """
    json_result = get_request(url, dealerId=str(kwargs["dealerId"]))

    results = []
    if json_result:
        if "reviews" in json_result:
            reviews = json_result["reviews"]
            for review in reviews:

                if "sentiment" in review:
                    sentiment = review["sentiment"]
                else:
                    sentiment = analyze_review_sentiments(review["review"])
                if review["purchase"]:
                    review_obj = DealerReview(
                        car_make=review["car_make"],
                        car_model=review["car_model"],
                        car_year=review["car_year"],
                        id=review["id"],
                        dealership=review["dealership"],
                        purchase_date=review["purchase_date"],
                        name=review["name"],
                        purchase=review["purchase"],
                        review=review["review"],
                        sentiment=sentiment,
                    )
                else:
                    review_obj = DealerReview(
                        car_make="",
                        car_model="",
                        car_year="",
                        id=review["id"],
                        dealership=review["dealership"],
                        purchase_date="",
                        name=review["name"],
                        purchase=review["purchase"],
                        review=review["review"],
                        sentiment=sentiment,
                    )
                results.append(vars(review_obj))
    return results
