"""
Cloud Function to get all reviews for a dealer id in Cloudant
"""

from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from typing import Dict, List, Union


def main(param_dict: Dict) -> Union[List[Dict], Dict]:
    """
    Main function that gets all reviews for a dealer id in Cloudant
    """
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
                
        data_fields = [
            "id",
            "name",
            "dealership",
            "review",
            "purchase",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year",
        ]
        
        docs = client["reviews"].get_query_result({"dealership": {"$eq": param_dict["dealerId"]}}, fields=data_fields)
        
        result = []
        for doc in docs:
            result.append(doc)
        if result:
            return result
        else:
            return {"error": "dealerId does not exist"}
        
    except CloudantException as ce:
        return {"error": ce}
    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        return {"error": err}
