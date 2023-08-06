"""
This module provides the Query class for fetching and processing queries from the EDC Alation API.

The module provides the following:

1. Constants for namespace name, service name, and timeouts.

2. The Query class, which provides a method `fetch_query` to fetch all the queries from an API and 
processes each query to fetch details, query text, and latest results. This method also handles 
exceptions, logs different stages of query processing, and reports if any error occurs.

The `fetch_query` method uses the Singleton design pattern to get instances of Logger and Tracer 
from the `environment_logging` and `environment_tracing` modules respectively. It also uses an 
instance of the `EnvironmentHttp` class from the `environment_http` module to make HTTP requests.

The module uses the requests library for making API requests and uses json and csv libraries for 
processing the API responses.

This module can be run as a standalone script or can be imported and used in other modules.

Imports:
    os
    sys
    requests
    json
    csv

    from data_ecosystem_services.cdc_admin_service import (
        environment_tracing as pade_env_tracing,
        environment_logging as pade_env_logging
    )

    from data_ecosystem_services.cdc_tech_environment_service import (
        environment_http as pade_env_http
    )

Constants:
    NAMESPACE_NAME (str): Name of the currently running file
    SERVICE_NAME (str): Name of the parent folder of the running file
    REQUEST_TIMEOUT (int): Timeout for requests in seconds
    TIMEOUT_ONE_MIN (int): Constant for a timeout of one minute in seconds
"""

import os
import sys
import json
import csv
import requests


from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_http as pade_env_http
)


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
REQUEST_TIMEOUT = 45
TIMEOUT_ONE_MIN = 60


class Query:
    """
    Query class is used for fetching and processing queries.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    fetch_query(edc_alation_api_token: str, edc_alation_base_url: str) -> None:
        Fetches all the queries from an API and processes each query to fetch details, query text, 
        and latest results. This method also handles exceptions, logs different stages of 
        query processing and reports if any error occurs.
    """

    def fetch_query_list(self, edc_alation_api_token, edc_alation_base_url, alation_datasource_id):
        """
        Fetches all the queries from an API and processes each query to fetch details, query text, 
        and latest results. This method also handles exceptions, logs different stages of 
        query processing and reports if any error occurs.

        Parameters:
        ----------
        edc_alation_api_token : str
            API token to access the EDC Alation API.

        edc_alation_base_url : str
            The base URL for the EDC Alation API.

        Returns:
        -------
        None

        Raises:
        ------
        Exception
            If an error occurs during the process of fetching and processing the queries.
        """

        headers = {"Token": edc_alation_api_token,
                   "Content-Type": "application/json", "accept": "application/json"}

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("fetch_query_list"):
            try:

                logger.info("Get query list")
                api_url = "/integration/v1/query/"
                query_list_url = edc_alation_base_url + api_url
                logger.info(f"query_list_url: {query_list_url}")
                obj_http = pade_env_http.EnvironmentHttp()
                params = {"datasource_id": alation_datasource_id}
                response_list = obj_http.get(query_list_url,
                                             headers=headers,
                                             timeout=TIMEOUT_ONE_MIN, params=params)

                return response_list

            except Exception as ex:
                error_msg = f"Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def fetch_query(self, edc_alation_api_token, edc_alation_base_url, alation_datasource_id, query_id):
        """
        Fetches all the queries from an API and processes each query to fetch details, query text, 
        and latest results. This method also handles exceptions, logs different stages of 
        query processing and reports if any error occurs.

        Parameters:
        ----------
        edc_alation_api_token : str
            API token to access the EDC Alation API.

        edc_alation_base_url : str
            The base URL for the EDC Alation API.

        Returns:
        -------
        None

        Raises:
        ------
        Exception
            If an error occurs during the process of fetching and processing the queries.
        """

        headers = {"Token": edc_alation_api_token,
                   "Content-Type": "application/json",
                   "accept": "application/json"}

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("fetch_query"):
            try:
                obj_http = pade_env_http.EnvironmentHttp()
                params = {"datasource_id": alation_datasource_id,
                          "limit": 1000}
                logger.info("##### Get all queries #####")
                api_url = "/integration/v1/query/"
                query_list_url = edc_alation_base_url + api_url
                logger.info(f"query_list_url: {query_list_url}")
                response = obj_http.get(query_list_url,
                                        headers=headers,
                                        timeout=TIMEOUT_ONE_MIN, params=params)
                queries = json.loads(response.text)
                for query in queries:
                    query_id = str(query["id"])
                    logger.info(
                        f"##### Get details for a single query {query_id} #####")
                    query_detail_url = edc_alation_base_url + api_url + query_id

                    response_detail = obj_http.get(query_detail_url,
                                                   headers=headers,
                                                   timeout=TIMEOUT_ONE_MIN, params=None)
                    query_detail = json.loads(response_detail.text)
                    detail = query_detail.get("detail")
                    logger.info(f"query_detail: {query_detail}")
                    if detail == "You do not have permission to perform this action.":
                        query_title = "No Permission"
                        logger.info(f"id: {query_id}, title: {query_title}")
                    else:
                        query_id = query_detail["query_id"]
                        logger.info(
                            f"query_id: {query_id}, title: {query_title}")

                # Get query text
                api_url = f"/integration/v1/query/{query_id}/sql/"
                query_text_url = edc_alation_base_url + api_url
                logger.info(f"query_text_url:{query_text_url}")
                response_query_text = requests.get(
                    query_text_url, headers=headers, timeout=TIMEOUT_ONE_MIN
                )
                response_content_text = "not_set"
                # Check the response status code to determine if the request was
                # successful
                if response_query_text.status_code in (200, 201):
                    # Extract the API token from the response
                    response_content_text = response_query_text.content.decode(
                        "utf-8")
                    # logger.info(f"SQL Query Text response: {query_text}")
                else:
                    logger.info(
                        "Failed to get SQL Query Text :" +
                        str(response_content_text)
                    )

                query_text = response_content_text
                query_text = query_text.replace("\n", " ").replace("'", "'")

                # Get latest result id
                api_url = f"/integration/v1/query/{query_id}/result/latest/"
                query_url = edc_alation_base_url + api_url
                logger.info(f"query_url: {query_url}")
                logger.info(f"headers: {headers}")
                # Send the request to the Alation API endpoint.
                # The endpoint for executing queries is `/integration/v1/query`.
                response_query = requests.get(query_url,
                                              headers=headers,
                                              timeout=TIMEOUT_ONE_MIN)
                logger.info(
                    "response_query.content:" +
                    response_query.content.decode("utf-8")
                )

                # execution_result_id = json_response['id']
                execution_result_id = "570"

                # Get lastest results and place in dataframe
                api_url = f"/integration/v1/result/{execution_result_id}/csv/"
                result_url = edc_alation_base_url + api_url

                # download and parse response as csv
                with requests.Session():
                    response_results = requests.get(
                        result_url, headers=headers, timeout=TIMEOUT_ONE_MIN
                    )
                    decoded_content = response_results.content.decode("utf-8")
                    logger.info("response_results.content:" + decoded_content)
                    csv_reader = csv.reader(
                        decoded_content.splitlines(), delimiter=","
                    )
                    logger.info.logger.info(list(csv_reader))

            except Exception as ex:
                error_msg = f"Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
