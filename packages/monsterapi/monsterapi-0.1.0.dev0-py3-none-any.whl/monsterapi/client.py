#MonsterAPIClient.py

"""
Monster API Python client to connect to LLM models on monsterapi

Base URL: https://api.monsterapi.ai/v1/generate/{model}

Available models:
-----------------

LLMs:
    1. falcon-7b-instruct
    2. falcon-40b-instruct
    3. mpt-30B-instruct
    4. mpt-7b-instruct
    5. openllama-13b-base
    6. llama2-7b-chat

Text to Image:
    1. stable-diffusion v1.5
    2. stable-diffusion XL V1.0

"""
import os
import time
import logging
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from typing import Optional, Literal, Union, List, Dict
from pydantic import BaseModel, Field

from monsterapi.InputDataModels import LLMInputModel1, LLMInputModel2, SDInputModel, MODELS_TO_DATAMODEL

# Use LOGGING_LEVEL environment variable to set logging level
# Default logging level is INFO
level = os.environ.get('LOGGING_LEVEL', 'INFO')

if level == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG)
elif level == 'INFO':
    logging.basicConfig(level=logging.INFO)
elif level == 'WARNING':
    logging.basicConfig(level=logging.WARNING)
elif level == 'ERROR':
    logging.basicConfig(level=logging.ERROR)
elif level == 'CRITICAL':
    logging.basicConfig(level=logging.CRITICAL)

logger = logging.getLogger(__name__)


class MClient():
    def __init__(self):
        self.boundary = '---011000010111000001101001'
        self.auth_token = os.environ.get('MONSTER_API_KEY')
        if not self.auth_token:
            raise ValueError("MONSTER_API_KEY environment variable not set!")
        self.headers = {
            "accept": "application/json",
            "content-type": f"multipart/form-data; boundary={self.boundary}",
            'Authorization': 'Bearer ' + self.auth_token}
        self.base_url = 'https://api.monsterapi.ai/v1'
        self.models_to_data_model = MODELS_TO_DATAMODEL

    def get_response(self, model:Literal['falcon-7b-instruct', 'falcon-40b-instruct', 'mpt-30B-instruct', 'mpt-7b-instruct', 'openllama-13b-base', 'llama2-7b-chat'], 
                     data: dict):
    
        if model not in self.models_to_data_model:
            raise ValueError(f"Invalid model: {model}!")

        dataModel = self.models_to_data_model[model](**data)
        url = f"{self.base_url}/generate/{model}"
        data = dataModel.dict()
        logger.info(f"Calling Monster API with url: {url}, with payload: {data}")

        # convert all values into string
        for key, value in data.items():
            data[key] = str(value)
        multipart_data = MultipartEncoder(fields=data, boundary=self.boundary)
        response = requests.post(url, headers=self.headers, data=multipart_data)
        response.raise_for_status()
        return response.json()
    
    def get_status(self, process_id):
        # /v1/status/{process_id}
        url = f"{self.base_url}/status/{process_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def wait_and_get_result(self, process_id, timeout=100):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time

            if elapsed_time >= timeout:
                raise TimeoutError(f"Process {process_id} timed out after {timeout} seconds.")

            status = self.get_status(process_id)
            if status['status'].lower() == 'completed':
                return status['result']
            elif status['status'].lower() == 'failed':
                raise RuntimeError(f"Process {process_id} failed! {status}")
            else:
                logger.debug(f"Process {process_id} is still running, status is {status['status']}. Waiting ...")
                time.sleep(0.01)