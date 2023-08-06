from .json_manifest import ManifestJson
from .db_column import Column
from pandas import json_normalize
from bs4 import BeautifulSoup

import json
from jsonschema import validate
import sys
import os
import pandas as pd
import requests


from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

import data_ecosystem_services.cdc_tech_environment_service.environment_file as pade_env_file
import data_ecosystem_services.alation_service.token as alation_token_endpoint

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

ENVIRONMENT = "dev"

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the project root directory by going up one or more levels
project_root = os.path.dirname(os.path.dirname(current_script_path))


class User:

    def convert_to_json_if_string(self, input_data):
        if isinstance(input_data, str):
            try:
                # Convert the JSON string to a Python dictionary
                parsed_data = json.loads(input_data)
                return parsed_data
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", str(e))
                return None
        else:
            # Handle non-string data based on your use case
            print("Input data is not a string.")
            return None

    def get_users_from_user_id_json(self, config, user_id_json):

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_users_from_user_id_json"):

            # Change the current working directory to the project root directory
            os.chdir(project_root)

            edc_alation_base_url = config.get("edc_alation_base_url")
            token_endpoint = alation_token_endpoint.TokenEndpoint(
                edc_alation_base_url)
            status_code, edc_alation_api_token, api_refresh_token = token_endpoint.get_api_token_from_config(
                config)

            logger.info(
                f"edc_alation_api_access_token_length: {str(len(edc_alation_api_token))}")
            logger.info(
                f"api_refresh_token_length: {str(len(api_refresh_token))}")

            # setting the base_url so that all we need to do is swap API endpoints
            base_url = edc_alation_base_url
            # api access key
            api_key = edc_alation_api_token
            # setting up this access key to be in the headers
            headers = {"token": api_key}
            # api for users
            api = "/integration/v2/user/"

            limit = 500
            skip = 0

            user_id_json = self.convert_to_json_if_string(user_id_json)

            # Extract the 'oid' values and convert them to strings
            oid_values = [str(item['oid']) for item in user_id_json]

            # Join the 'oid' values with '&' separator
            id_string = '&'.join([f"id={oid}" for oid in oid_values])

            # Create a dictionary to hold the parameters
            params = {}
            params['limit'] = limit
            params['skip'] = skip
            params['id'] = id_string

            # make the API call
            tables_result = requests.get(
                base_url + api, headers=headers, params=params)
            # convert the response to a python dict.
            tables_result_json = tables_result.json()

            # Process the data
            expanded_json = []
            for item in tables_result_json:
                new_item = item.copy()  # start with existing fields
                for field in item['custom_fields']:
                    # add custom fields
                    new_item[field['field_name']] = field['value']
                expanded_json.append(new_item)

            # Convert to dataframe
            df_tables = json_normalize(expanded_json)

            return df_tables
