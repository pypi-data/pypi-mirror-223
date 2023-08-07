import os
import sys
import json
import urllib.parse

import requests
from loguru import logger

from .models import *

logger.remove()
logger.add(sys.stdout, colorize=True, 
           format="<le>[{time:DD-MM-YYYY HH:mm:ss}]</le> <lvl>[{level}]: {message}</lvl>", 
           level="INFO")


class SolORM:
    base_url = None

    verify_ssl_certificates = True

    # Add Methods
    add_paths = {
        TIC.__name__: "TICs/add",
        TAC.__name__: "TACs/add",
        SpotPublishedTIC.__name__: "SpotPublishedTICs/add",
        SpotEstimatedTIC.__name__: "SpotEstimatedTICs/add",
        ReceivedForecast.__name__: "ReceivedForecasts/add",
        SAMParameter.__name__: "SAMParameters/add",
        OptimizationParameter.__name__: "OptimizationParameters/add",
        MeasuredWeather.__name__:"MeasuredWeathers/add",
        MeasuredWeatherTIC.__name__: "MeasuredWeatherTICs/add"
    }

    # Get Methods
    get_paths = {
        TIC.__name__: "TICs",
        TAC.__name__: "TACs",
        SpotPublishedTIC.__name__: "SpotPublishedTICs",
        SpotEstimatedTIC.__name__: "SpotEstimatedTICs",
        ReceivedForecast.__name__ : "ReceivedForecasts",
        SAMParameter.__name__: "SAMParameters",
        OptimizationParameter.__name__: "OptimizationParameters",
        MeasuredWeather.__name__:"MeasuredWeathers",
        MeasuredWeatherTIC.__name__: "MeasuredWeatherTICs"
    }

    # Util Methods
    util_paths = {
        'CreateTICsAndTACs': "Utilities/CreateTICsAndTACs"
    }

    def __init__(self, base_url=None, debug=False):
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = os.getenv("DB_API_URL")
            if self.base_url is None:
                raise Exception("DB_API_URL environment variable not set")
        if debug:
            logger.remove()
            logger.add(sys.stdout, colorize=True, 
                       format="<le>[{time:DD-MM-YYYY HH:mm:ss}]</le> <lvl>[{level}]: {message}</lvl>", 
                       level="DEBUG")
    
    def get_url(self, path):
        return urllib.parse.urljoin(self.base_url, path)
    
    def add_entity(self, entity):
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        response = requests.post(
            self.get_url(
                self.add_paths[entity.__class__.__name__]),
                json.dumps(entity.dict(exclude_none=True)), headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 201:
            logger.debug("Request successful")
            return json.loads(response.text)
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
    
    def get_entity(self, entity_name, id, id2=None):
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        endpoint = self.get_url(self.get_paths[entity_name]) + "/" + str(id) + ("/" + str(id2) if id2 is not None else "")        
        response = requests.get(endpoint, headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 200:
            logger.debug("Request successful")
            return json.loads(response.text)
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
    
    def get_last_entity(self, entity_name, number=1):
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        endpoint = self.get_url(self.get_paths[entity_name]) + "/getLast/" + str(number)
        response = requests.get(endpoint, headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 200:
            logger.debug("Request successful")
            return json.loads(response.text)
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
    
    def get_since_entity(self, entity_name, since, number=10):
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        endpoint = self.get_url(self.get_paths[entity_name]) + "/getSince/" + str(since) + "/" + str(number)
        response = requests.get(endpoint, headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 200:
            logger.debug("Request successful")
            return json.loads(response.text)
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
        
    def util_create_TIC_TACs(self, years = 1):
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        endpoint = self.get_url(self.util_paths['CreateTICsAndTACs'])

        response = requests.post(
            endpoint,
            json.dumps({"years": years}), headers=headers, verify = self.verify_ssl_certificates)
        
        if response.status_code == 201:
            logger.debug("Request successful")
            return json.loads(response.text)
        else:
            logger.debug(f"{response.status_code}-{response.reason}\n{response.text}")
            raise Exception(f"Request failed with status {response.status_code}")
    