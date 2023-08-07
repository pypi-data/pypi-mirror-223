from typing import Union, List
from .common import Valid, Error

def is_url_valid(url: str) -> Union[Valid, List[Error]]:
    return Valid()