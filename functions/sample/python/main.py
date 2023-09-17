"""
IBM Cloud Function that gets all databases for a Cloudant instance
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from typing import Dict


def main(param_dict: Dict) -> Dict:
    """
    Main function that gets all databases for a Cloudant instance

    Args:
        param_dict (Dict): input paramaters
        
    Example:
        >>> main({
            "COUCH_USERNAME": "username",
            "IAM_API_KEY": "apikey"
        })
    """
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
