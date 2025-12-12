import requests
from typing import Tuple, Optional, Dict, Any, List

# API Configuration
GATEWAY_URL = "http://api_gateway:5001"
REQUEST_TIMEOUT = 5


def api_get(endpoint: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Perform GET request to API gateway"""
    try:
        response = requests.get(f"{GATEWAY_URL}{endpoint}", timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            return response.json(), None
        
        return None, f"Error: {response.status_code} - {response.text}"
        
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to the server. Please check your connection."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def api_post(endpoint: str, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Perform POST request to API gateway"""
    try:
        response = requests.post(
            f"{GATEWAY_URL}{endpoint}",
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code in (200, 201):
            return response.json(), None
        
        return None, f"Error: {response.status_code} - {response.text}"
        
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to the server. Please check your connection."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def api_delete(endpoint: str) -> Tuple[bool, Optional[str]]:
    """Perform DELETE request to API gateway"""
    try:
        response = requests.delete(f"{GATEWAY_URL}{endpoint}", timeout=REQUEST_TIMEOUT)
        
        if response.status_code in (200, 204):
            return True, None
        
        return False, f"Error: {response.status_code} - {response.text}"
        
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return False, "Unable to connect to the server. Please check your connection."
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def check_api_health() -> Tuple[bool, str]:
    """Check if API gateway is reachable"""
    try:
        response = requests.get(f"{GATEWAY_URL}/health", timeout=2)
        
        if response.status_code == 200:
            return True, "API Gateway is online"
        
        return False, f"API Gateway returned status {response.status_code}"
        
    except requests.exceptions.Timeout:
        return False, "API Gateway is not responding"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API Gateway"
    except Exception as e:
        return False, f"Health check failed: {str(e)}"