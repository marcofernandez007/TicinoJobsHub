import requests
from flask import current_app
import os

# Get the API endpoint and key from environment variables
API_ENDPOINT = os.environ.get('TICINO_BUSINESS_API_ENDPOINT', 'https://api.ticino-business-directory.ch')
API_KEY = os.environ.get('TICINO_BUSINESS_API_KEY', '')

def verify_business(company_name, vat_number):
    """
    Verify a business using the Ticino business directory API.
    """
    verify_url = f"{API_ENDPOINT}/verify"
    
    try:
        response = requests.post(verify_url, 
                                 json={"company_name": company_name, "vat_number": vat_number},
                                 headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "verified":
            return True, "Business verified successfully"
        else:
            return False, result.get("message", "Unable to verify business")
    except requests.RequestException as e:
        current_app.logger.error(f"Error verifying business: {str(e)}")
        return False, "Error occurred during verification"

def get_business_details(vat_number):
    """
    Retrieve business details from the Ticino business directory API.
    """
    details_url = f"{API_ENDPOINT}/business/{vat_number}"
    
    try:
        response = requests.get(details_url, headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        current_app.logger.error(f"Error retrieving business details: {str(e)}")
        return None

def search_businesses(query):
    """
    Search for businesses in the Ticino business directory.
    """
    search_url = f"{API_ENDPOINT}/search"
    
    try:
        response = requests.get(search_url, 
                                params={"q": query},
                                headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        current_app.logger.error(f"Error searching businesses: {str(e)}")
        return None
