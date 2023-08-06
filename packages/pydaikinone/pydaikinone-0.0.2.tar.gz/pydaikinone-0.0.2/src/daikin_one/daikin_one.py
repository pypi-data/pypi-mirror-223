import requests
import json
from api_contracts import *

class DaikinOneAPI:
    DAIKIN_ONE_ENDPOINT = "https://integrator-api.daikinskyport.com"
    AUTH_PATH = "/v1/token"
    DEVICES_PATH = "/v1/devices"

    auth_token: DaikinOneAccessToken = None

    email: str
    integrator_token: str
    api_key: str

    def __init__(self, email, integrator_token, api_key):
        self.email = email
        self.integrator_token = integrator_token
        self.api_key = api_key

    def __get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.auth_token.access_token,
            "x-api-key": self.api_key
        }
    
    def __refresh_token(self):

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        auth_request = {
            "email": self.email,
            "integratorToken": self.integrator_token
        }

        auth_response = requests.post(self.DAIKIN_ONE_ENDPOINT + self.AUTH_PATH, data=json.dumps(auth_request), headers=headers)

        auth_response.raise_for_status()
        auth_response_json = auth_response.json();
        self.auth_token = DaikinOneAccessToken.from_dict(auth_response_json)

    def __handle_auth(self):
        if self.auth_token is None or self.auth_token.is_expired():
            self.__refresh_token()

    def get_locations(self) -> List[DaikinOneLocation]:
        self.__handle_auth()
        
        locations_response = requests.get(self.DAIKIN_ONE_ENDPOINT + self.DEVICES_PATH, headers=self.__get_headers())
        locations_response.raise_for_status()
        locations: List[DaikinOneLocation] = DaikinOneLocation.from_json(locations_response.text)
        
        return locations
    
    def get_thermostat(self, device_id: str) -> DaikinOneThermostat:
        self.__handle_auth()
        device_details_response = requests.get(self.DAIKIN_ONE_ENDPOINT + self.DEVICES_PATH + "/" + device_id, headers=self.__get_headers())
        device_details_response.raise_for_status()
        device_details: DaikinOneThermostat = DaikinOneThermostat.from_json(device_details_response.text)

        return device_details