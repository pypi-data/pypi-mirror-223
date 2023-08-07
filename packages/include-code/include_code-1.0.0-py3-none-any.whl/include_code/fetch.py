import requests
from .common import Error
from typing import Union, List

def fetch(url: str) -> Union[str, Error]:
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as request_exception:
        return Error(f"[ERROR][FETCHING]: {request_exception} \n")
    return req.text
