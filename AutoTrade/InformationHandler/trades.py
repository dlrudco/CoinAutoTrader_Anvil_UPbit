from .accounts import *
from utils import payload 

import requests
from typing import List

creds = credentials()

__all__ = ['check_chance', 'check_single_order_status', 'check_all_orders_by_state', 'check_all_orders_by_ids']

def check_chance(market):
    params = {
    'market': market,
    }
    
    headers = payload.encode_payload(params)

    res = requests.get(creds.server_url + '/v1/orders/chance', params=params, headers=headers)
    return res.json()


def check_single_order_status(uuid=None, identifier=None):
    assert uuid or identifier, 'uuid or identifier must be provided'
    assert not (uuid and identifier), 'uuid and identifier cannot be provided at the same time'
    
    params = {'uuid': uuid} if uuid else {'identifier': identifier}
    headers = payload.encode_payload(params)

    res = requests.get(creds.server_url + '/v1/order', params=params, headers=headers)
    return res.json()

def check_all_orders_by_state(market, state : str = None, states: List[str] = None, page: int = 1, limit: int = 100):
    assert state or states, 'state or states must be provided'
    assert not (state and states), 'state and states cannot be provided at the same time'
    
    params = {'states[]': states} if states else {'state': state}
    
    headers = payload.encode_payload(params)

    res = requests.get(creds.server_url + '/v1/orders', params=params, headers=headers)
    return res.json()

    
def check_all_orders_by_ids(market, uuids: List[str] = None, identifiers : List[str] = None, page: int = 1, limit: int = 100):
    assert uuids or identifiers, 'uuids or identifiers must be provided'
    assert not (uuids and identifiers), 'uuids and identifiers cannot be provided at the same time'
    
    params = {'uuids[]': uuids} if uuids else {'identifiers[]': identifiers}
    
    headers = payload.encode_payload(params)

    res = requests.get(creds.server_url + '/v1/orders', params=params, headers=headers)
    return res.json()

if __name__ == "__main__":
    breakpoint()