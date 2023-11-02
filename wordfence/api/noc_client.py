import requests
from urllib.parse import urlencode

from .licensing import License
from .exceptions import ApiException
from ..util.validation import Validator, ValidationException

DEFAULT_TIMEOUT = 180


class NocClient:

    def __init__(
                self,
                license: License,
                base_url: str = None,
                timeout: int = DEFAULT_TIMEOUT
            ):
        self.license = license
        self.base_url = base_url \
            if base_url is not None \
            else self.get_default_base_url()
        self.timeout = timeout

    def get_default_base_url(self) -> str:
        raise ApiException('No default base URL is defined')

    def build_query(self, action: str, base_query: dict = None) -> dict:
        if base_query is None:
            query = {}
        else:
            query = base_query.copy()
        query['action'] = action
        query['k'] = self.license.key
        query['cli'] = 1
        return query

    def request(self, action: str, query: dict = None):
        query = self.build_query(action, query)
        url = self.base_url + '?' + urlencode(query)
        try:
            response = requests.get(url, timeout=self.timeout)
            return response.json()
        except Exception as error:
            raise ApiException('Request failed') from error

    def validate_response(self, response, validator: Validator) -> None:
        try:
            validator.validate(response)
        except ValidationException as exception:
            raise ApiException('Response validation failed') from exception
