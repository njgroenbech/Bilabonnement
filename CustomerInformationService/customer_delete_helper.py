import requests

def delete_customer_contracts(customer_id):
    # get all contracts
    contracts_response = requests.get(
        "http://contract-service:5004/contracts", 
        timeout=3
    )
    
    if contracts_response.status_code != 200:
        raise Exception("Failed to fetch contracts")
    
    # filter and delete contracts for this customer
    contracts = contracts_response.json()
    
    for contract in contracts:
        if contract['customer_id'] == customer_id:

            # free up the car
            requests.patch(
                f'http://carfleet-service:5003/cars/{contract["car_id"]}/status',
                json={"status": "available"},
                timeout=3
            )
            
            # Delete contract
            requests.delete(
                f'http://contract-service:5004/contracts/{contract["contract_id"]}',
                timeout=3
            )