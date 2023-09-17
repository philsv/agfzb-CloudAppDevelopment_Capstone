"""
IBM Cloud Function that creates a document in a Cloudant database
"""

from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict: dict) -> dict:
    """
    Main function that creates a review for a product in Cloudant
    """
    try:
        client = Cloudant.iam(account_name=param_dict["COUCH_USERNAME"], api_key=param_dict["IAM_API_KEY"], connect=True)
        my_document = client["reviews"].create_document(param_dict["review"])

        if my_document.exists():
            print("Successfully created document.")

    except CloudantException as ce:
        return {"error": ce}

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        return {"error": err}
    return {"success": True}
