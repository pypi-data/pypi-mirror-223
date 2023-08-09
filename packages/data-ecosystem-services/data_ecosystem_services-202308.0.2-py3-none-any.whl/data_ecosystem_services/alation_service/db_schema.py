import requests
import json
import os
import sys
import concurrent.futures
import platform
import datetime
from .token import TokenEndpoint
from .custom_fields import CustomFieldsEndpoint
from .tags import TagsEndpoint
from .id_finder import IdFinderEndpoint
from .datasource import DataSource
from .json_manifest import ManifestJson
from .excel_manifest import ManifestExcel
from .db_table import Table

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as cdc_env_file,
    environment_http as cdc_env_http
)

import data_ecosystem_services.alation_service.excel_manifest as alation_manifest_excel
import data_ecosystem_services.alation_service.db_table as alation_table

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
TIMEOUT_ONE_MIN = 60  # or set to whatever value you want

# We have implementing batching and multithreading
# Because average calls before force_submit is milliseconds
# Multi-threading is not really helping much at all
# So set to lower number 4
if platform.system() != 'Windows':
    NUM_THREADS_MAX = 4
else:
    NUM_THREADS_MAX = 4

ENCODE_PERIOD = False
REQUEST_TIMEOUT = 45


class EdcAlationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Schema:
    """
    A base class for interacting with Alation Schema. 
    """

    @staticmethod
    def get_schema(edc_alation_api_token, edc_alation_base_url, alation_schema_id):
        """ 
        Retrieves details for a specific schema from Alation using the provided schema ID.

        Args:
            edc_alation_api_token (str): Headers to be used in the request, typically including authentication information.
            edc_alation_base_url (str): The base URL of the Alation instance.
            alation_schema_id (int): ID of the Alation schema to retrieve.

        Returns:
            dict: A dictionary containing details of the schema.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_schema"):

            try:

                # Log the parameters
                logger.info("edc_alation_api_token length: %s",
                            str(len(edc_alation_api_token)))
                logger.info("alation_schema_id: %s", str(alation_schema_id))
                logger.info("edc_alation_base_url: %s",
                            str(edc_alation_base_url))
                schema_id = alation_schema_id

                # Set the headers for the request
                headers = {"accept": "application/json",
                           'Token': edc_alation_api_token}

                # Set the default values for the limit and skip parameters
                limit = 100
                skip = 0

                # Create a dictionary to hold the parameters
                params = {}
                params['limit'] = limit
                params['skip'] = skip
                params['id'] = schema_id
                api_url = f"{edc_alation_base_url}/integration/v2/schema/"
                logger.info(f"api_url: {api_url}")
                logger.info(f"params: {str(params)}")
                # Make the schema request to Alation
                obj_http = cdc_env_http.EnvironmentHttp()
                response_schema = obj_http.get(
                    api_url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
                response_schema_json = response_schema.json()

                # Check the response status code to determine if successful
                if len(response_schema_json) == 1:
                    schema_result = response_schema_json[0]

                    response_schema_text = "not_set"
                    datasource_id = -1
                    if "title" in schema_result:
                        datasource_id = schema_result.get("ds_id")
                        pade_datasource = DataSource()
                        response_datasource = pade_datasource.get_datasource(
                            edc_alation_api_token, edc_alation_base_url, datasource_id)
                        datasource_result = response_datasource.json()
                        return response_schema, datasource_result
                    else:
                        response_schema_text = schema_result.get("reason")
                        error_msg = "Failed to get schema:" + \
                            str(response_schema_text)
                        error_msg = error_msg + \
                            " for api_url: " + str(api_url)
                        error_msg = error_msg + \
                            " for schema_id: " + str(schema_id)
                        error_msg = error_msg + \
                            " and datasource_id: " + str(datasource_id)
                        error_msg = error_msg + \
                            " and schema_result: " + str(schema_result)
                        logger.error(error_msg)
                        raise EdcAlationError(error_msg)
                else:
                    error_msg = "Failed to get schema_result"
                    raise EdcAlationError(error_msg)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_schema_tables(edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_schema_id):
        """ 
        Get list of tables for this schema from the provided Alation URL, like: "https://alation_domain/integration/v2/table/?limit=100000&skip=0".

        Args:
            edc_alation_api_token (str): Headers to be used in the request, typically including authentication information.
            edc_alation_base_url (str): The base URL of the Alation instance.
            alation_datasource_id (int): ID of the Alation data source.
            alation_schema_id (int): ID of the Alation schema.

        Returns:
            list: List of tables in the schema. Each table is represented as a dictionary.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()
        with tracer.start_as_current_span("get_schema_tables"):

            try:

                # Set the headers for the request
                headers = {"accept": "application/json",
                           'Token': edc_alation_api_token}

                limit = 500
                skip = 0

                # Create a dictionary to hold the parameters
                params = {}
                params['limit'] = limit
                params['skip'] = skip
                params['schema_id'] = alation_schema_id
                params['ds_id'] = alation_datasource_id

                obj_environment_http = cdc_env_http.EnvironmentHttp()
                api_url = f"{edc_alation_base_url}/integration/v2/table/"
                response = obj_environment_http.get(api_url, headers=headers, params=params,
                                                    timeout=REQUEST_TIMEOUT)
                # Go through all tables listed for this schema and add to our manifest template
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                tables_dict = {}
                response_json = response.json()  # Convert to JSON
                for table_to_process in response_json:
                    # Assuming table_to_process is the object causing the error
                    if isinstance(table_to_process, dict):
                        table_name = table_to_process.get('name')
                        if table_name:
                            tables_dict[table_name] = table_to_process
                    else:
                        # Handle the case when table_to_process is not a dictionary
                        error_msg = f"Invalid table_to_process object: {table_to_process}"
                        raise ValueError(error_msg)
                return tables_dict
            except json.JSONDecodeError as err:
                error_msg = f"JSON Decode occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.HTTPError as err:
                error_msg = f"HTTP Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.ConnectionError as err:
                error_msg = f"Connection Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.Timeout as err:
                error_msg = f"Timeout Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.RequestException as err:
                error_msg = f"An error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_table_columns(edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_schema_id, alation_table_id):
        """ 
        Get the list of columns for a specific table in the Alation instance.

        Args:
            edc_alation_api_token (str): The API token for authenticating with the Alation instance.
            edc_alation_base_url (str): The base URL of the Alation instance.
            alation_schema_id (int): The ID of the Alation schema.
            alation_datasource_id (int): The ID of the Alation data source.
            alation_table_id (int): The ID of the Alation table.

        Returns:
            list: The list of columns for the specified table. Each column is represented as a dictionary.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_table_columns"):

            column_to_process = {}

            try:

                # Set the headers for the API request
                headers = {"accept": "application/json"}
                headers["Token"] = edc_alation_api_token

                limit = 1000
                skip = 0

                # Set the parameters for the API request
                params = {}
                params['limit'] = limit
                params['skip'] = skip
                params['schema_id'] = alation_schema_id
                params['ds_id'] = alation_datasource_id
                params['table_id'] = alation_table_id

                # Create the API URL
                api_url = f"{edc_alation_base_url}/integration/v2/column/"

                # Log Parameters
                logger.info(f"api_url: {api_url}")
                logger.info(f"params: {str(params)}")

                # Make the API request
                obj_http = cdc_env_http.EnvironmentHttp()
                response_columns = obj_http.get(
                    api_url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)

                # Go through all tables listed for this schema and add to our manifest template
                # Convert to Python object
                response_columns_json = response_columns.json()

                columns_dict = {}
                for column_to_process in response_columns_json:
                    columns_dict[column_to_process['name']] = column_to_process
                return columns_dict

            except Exception as ex:
                error_msg = "Error: %s: %s", ex, str(column_to_process)
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_excel_manifest_file_path_temp(upload_or_download, repository_path, environment, alation_user_id):
        """
        Constructs a temporary path for an Excel manifest file based on various parameters and the current date/time.

        Args:
            upload_or_download (str): Denotes whether the action is an 'upload' or 'download'.
            repository_path (str): The path to the directory where the Excel manifest file will be stored.
            environment (str): Specifies the environment under which the file is being managed.
            alation_user_id (str): Unique identifier of an Alation user.

        Returns:
            str: The full path to the temporary Excel manifest file.

        Raises:
            Exception: If an error occurs during the construction of the Excel file path.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_excel_manifest_file_path_temp"):
            try:

                # Get current time
                current_date = datetime.datetime.now()

                yyyy_string = current_date.year
                mm_string = current_date.month
                dd_string = current_date.day
                # Format as a 24-hour time string
                time_str = current_date.strftime("%H_%M_%S")

                datasource_title = "temp"
                schema_name = "manifest"

                obj_file = cdc_env_file.EnvironmentFile()

                file_name = (
                    obj_file.scrub_file_name(datasource_title)
                    + "_"
                    + obj_file.scrub_file_name(schema_name)
                    + str(yyyy_string)
                    + "_"
                    + str(mm_string)
                    + "_"
                    + str(dd_string)
                    + "_"
                    + str(time_str)
                    + "_" + str(alation_user_id) + "_" +
                    upload_or_download + ".xlsx"
                )

                right_most_200_chars = file_name[-200:]
                file_name = right_most_200_chars

                manifest_path = (
                    repository_path + "/" + environment + "_manifest" +
                    "_" + upload_or_download + "s" + "/"
                )
                manifest_path = obj_file.convert_to_current_os_dir(
                    manifest_path)
                logger.info("manifest_path: " + manifest_path)

                manifest_excel_file = manifest_path + file_name
                logger.info("manifest_excel_file: " + manifest_excel_file)

                return manifest_excel_file
            except Exception as ex:
                # Corrected error message formatting
                error_msg = f"Excel Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_excel_manifest_file_path(upload_or_download, repository_path, datasource_title, schema_name, environment, alation_user_id):
        """_summary_

        Args:
            upload_or_download (_type_): _description_
            yyyy (_type_): _description_
            mm (_type_): _description_
            dd (_type_): _description_
            repository_path (_type_): _description_
            datasource_title (_type_): _description_
            schema_name (_type_): _description_
            environment (_type_): _description_
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_excel_manifest_file_path"):
            try:

                # Get current time
                current_date = datetime.datetime.now()

                yyyy_string = current_date.year
                mm_string = current_date.month
                dd_string = current_date.day
                # Format as a 24-hour time string
                time_str = current_date.strftime("%H_%M_%S")

                if schema_name == 'object_name_is_missing' or schema_name == 'object name is missing':
                    raise ValueError('Invalid schema_name value.')

                obj_file = cdc_env_file.EnvironmentFile()

                file_name = (
                    obj_file.scrub_file_name(datasource_title)
                    + "_"
                    + obj_file.scrub_file_name(schema_name)
                    + str(yyyy_string)
                    + "_"
                    + str(mm_string)
                    + "_"
                    + str(dd_string)
                    + "_"
                    + str(time_str)
                    + "_" + str(alation_user_id) + "_" +
                    upload_or_download + ".xlsx"
                )

                right_most_200_chars = file_name[-200:]
                file_name = right_most_200_chars

                manifest_path = (
                    repository_path + "/" + environment + "_manifest" +
                    "_" + upload_or_download + "s" + "/"
                )
                manifest_path = obj_file.convert_to_current_os_dir(
                    manifest_path)
                logger.info("manifest_path: " + manifest_path)

                manifest_excel_file = manifest_path + file_name
                logger.info("manifest_excel_file: " + manifest_excel_file)

                return manifest_excel_file
            except Exception as ex:
                # Corrected error message formatting
                error_msg = f"Excel Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_json_manifest_file_path(upload_or_download, repository_path, datasource_title, schema_name, environment, alation_user_id):
        """Get the file name for the manifest JSON file.

        Args:
            upload_or_download (str): The type of operation, whether "upload" or "download".
            repository_path (str): The path to the repository.
            datasource_title (str): The title of the data source.
            schema_name (str): The name of the schema.
            environment (str): The environment name.
            alation_user_id (str): The ID of the Alation user.

        Returns:
            str: The file name for the manifest JSON file.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_manifest_file_name"):
            try:

                # Get current time
                current_date = datetime.datetime.now()

                yyyy_string = current_date.year
                mm_string = current_date.month
                dd_string = current_date.day
                # Format as a 24-hour time string
                time_str = current_date.strftime("%H_%M_%S")

                if schema_name == 'object_name_is_missing' or schema_name == 'object name is missing':
                    raise ValueError('Invalid schema_name value.')

                obj_file = cdc_env_file.EnvironmentFile()

                manifest_path = (
                    repository_path + "/" + environment + "_manifest" +
                    "_" + upload_or_download + "s" + "/"
                )

                logger.info("manifest_path: " + manifest_path)

                file_name = (
                    obj_file.scrub_file_name(datasource_title)
                    + "_"
                    + obj_file.scrub_file_name(schema_name)
                    + str(yyyy_string)
                    + "_"
                    + str(mm_string)
                    + "_"
                    + str(dd_string)
                    + "_"
                    + str(time_str)
                    + "_" + str(alation_user_id) + "_" +
                    upload_or_download + ".json"
                )

                right_most_200_chars = file_name[-200:]
                file_name = right_most_200_chars

                manifest_path = obj_file.convert_to_current_os_dir(
                    manifest_path)
                manifest_file = manifest_path + file_name

                logger.info(f"manifest_file: {manifest_file}")

                return manifest_file
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_json_schema_file_path(repository_path, environment):
        """
        Get the file path for the 'manifest.schema.json' file associated with the specified environment.

        This method constructs the file path for the 'manifest.schema.json' file based on the provided
        repository_path and environment. The file is expected to be located in the schema directory of the specified environment.

        Args:
            repository_path (str): The path to the repository containing the schema directories.
            environment (str): The name of the environment to which the schema belongs.

        Returns:
            str: The file path for the 'manifest.schema.json' file.

        Raises:
            Exception: If any error occurs during the file path construction.

        Note:
            This method assumes that the 'manifest.schema.json' file is located within the schema directory
            of the specified environment.

        Example:
            repository_path = '/path/to/repository'
            environment = 'dev'
            json_schema_file_path = get_json_schema_file_path(repository_path, environment)
            print(json_schema_file_path)
            # Output: '/path/to/repository/dev_schema/manifest.schema.json'
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_json_schema_file_path"):
            try:
                obj_file = cdc_env_file.EnvironmentFile()
                schema_path = (repository_path + "/" + environment + "_schema")
                logger.info("schema_path: " + schema_path)
                file_name = "manifest.schema.json"

                schema_path = obj_file.convert_to_current_os_dir(
                    schema_path)

                # Join the directory path with the filename
                json_schema_file_path = os.path.join(schema_path, file_name)

                logger.info(
                    f"json_schema_file_path: {json_schema_file_path}")

                return json_schema_file_path

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_excel_schema_file_path(repository_path, environment):
        """
        Get the file path for the 'get_excel_schema_file_path.xlsx' file associated with the specified environment.

        This method constructs the file path for the 'excel_manifest_schema_for_tables_sql.xlsx' file based on the provided
        repository_path and environment. The file is expected to be located in the schema directory of the specified environment.

        Args:
            repository_path (str): The path to the repository containing the schema directories.
            environment (str): The name of the environment to which the schema belongs.

        Returns:
            str: The file path for the 'excel_manifest_schema_for_tables_sql.xlsx' file.

        Raises:
            Exception: If any error occurs during the file path construction.

        Note:
            This method assumes that the 'excel_manifest_schema_for_tables_sql.xlsx' file is located within the schema directory
            of the specified environment.

        Example:
            repository_path = '/path/to/repository'
            environment = 'dev'
            excel_schema_file_path = get_excel_schema_file_path(repository_path, environment)
            print(excel_schema_file_path)
            # Output: '/path/to/repository/dev_schema/excel_manifest_schema_for_tables_sql.xlsx'
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_excel_schema_file_path"):
            try:
                obj_file = cdc_env_file.EnvironmentFile()
                schema_path = (repository_path + "/" + environment + "_schema")

                schema_path = obj_file.convert_to_current_os_dir(
                    schema_path)

                logger.info("schema_path: " + schema_path)
                schema_xls_file = "excel_manifest_schema_for_tables_sql.xlsx"

                # Join the directory path with the filename
                excel_schema_file_path = os.path.join(
                    schema_path, schema_xls_file)

                logger.info(
                    f"excel_schema_file_path: {excel_schema_file_path}")

                return excel_schema_file_path
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def download_schema_manifest_excel_file(cls, alation_schema_id, config, json_schema_file_path):
        """
        Downloads the schema manifest Excel file for a given Alation schema ID.

        This method generates the Excel file data using the `generate_excel_file_data` method of the 
        `alation_manifest_excel.ManifestExcel` class, then generates the Excel file using the 
        `generate_excel_file_from_data` method of the same class.

        Parameters
        ----------
        alation_schema_id : int
            The ID of the Alation schema for which to download the manifest Excel file.
        config : dict
            The configuration parameters for the operation.

        Returns
        -------
        str
            The path to the downloaded manifest Excel file.

        Raises
        ------
        Exception
            If an error occurs during the operation, an exception is raised and logged.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("download_schema_manifest"):

            try:
                logger.info("alation_schema_id: " + str(alation_schema_id))

                table = alation_table.Table(None, json_schema_file_path)

                manifest_excel = alation_manifest_excel.ManifestExcel()
                df_schema, df_table_list, manifest_excel_file, columns_to_hide, df_fields_excel_schema = manifest_excel.generate_excel_file_data(
                    alation_schema_id, config, json_schema_file_path)

                df_status, schema_file = table.get_valueset_for_tables_sql_xlsx(
                    "Status of Dataset")
                df_access_level, schema_file = table.get_valueset_for_tables_sql_xlsx(
                    "Access Level")
                df_format, schema_file = table.get_valueset_for_tables_sql_xlsx(
                    "Format")
                df_language, schema_file = table.get_valueset_for_tables_sql_xlsx(
                    "Language")
                df_steward, schema_file = table.get_valueset_for_tables_sql_xlsx(
                    "steward")
                df_update_frequency, schema_file = table.get_valueset_for_tables_sql_xlsx(
                    "update_frequency")

                manifest_excel_file = manifest_excel.generate_excel_file_from_data(
                    config, columns_to_hide, df_table_list, manifest_excel_file, df_status, df_steward, df_access_level, df_language, df_update_frequency, df_format, df_fields_excel_schema)

                return manifest_excel_file

                # Get the data source title from
            except Exception as ex:
                error_msg = "Excel Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def download_schema_manifest_json_file(cls, alation_schema_id, config):
        """
        Downloads the schema manifest for a given Alation schema ID using provided configuration.

        This method retrieves the schema manifest from an Alation instance. The manifest contains
        detailed information about the schema, including data types, relations, and other properties.

        Args:
            alation_schema_id (int): The unique identifier for the schema in the Alation system. 
            This ID is used to locate the specific schema for which the manifest is required.

            config (dict): A configuration dictionary containing necessary parameters for connecting
            to the Alation instance. This might include authentication details and network configurations.

        Returns:
            dict: The schema manifest represented as a dictionary. The keys and values in this dictionary 
            represent properties of the schema and their corresponding values as present in the Alation system.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        schema_id = alation_schema_id
        schema_name = None

        with tracer.start_as_current_span("download_schema_manifest"):
            try:

                # Get configuration parameteres
                environment = config.get("environment")
                edc_alation_base_url = config.get("edc_alation_base_url")
                repository_path = config.get("repository_path")
                alation_user_id = config.get("edc_alation_user_id")

                # Log the configuration parameters
                logger.info(f"edc_alation_base_url: {edc_alation_base_url}")
                logger.info(f"environment: {environment}")
                logger.info(f"schema_id: {schema_id}")

                if not edc_alation_base_url:
                    raise ValueError(
                        "edc_alation_base_url is not set in config.")

                # Get the Alation API Access Token
                token_endpoint = TokenEndpoint(edc_alation_base_url)
                status_code, edc_alation_api_token, api_refresh_token = token_endpoint.get_api_token_from_config(
                    config)
                logger.info(f"status_code: {status_code}")
                logger.info(
                    f"edc_alation_api_token length:{str(len(edc_alation_api_token))}")
                if len(edc_alation_api_token.strip()) == 0:
                    msg = "Alation API Access Token is not set"
                    logger.error(msg)
                    raise ValueError(msg)

                # Get the schema and datasource details
                schema_result, datasource_result = cls.get_schema(
                    edc_alation_api_token, edc_alation_base_url, schema_id
                )

                schema_result_json = schema_result.json()

                # Set the schema name, datasource title and datasource_id
                schema_name = schema_result_json[0].get("name")
                datasource_title = datasource_result.get("title")
                datasource_id = datasource_result.get("id")
                alation_datasource_id = datasource_id

                # Log the schema details
                logger.info(
                    f"schema_result length: {str(len(schema_result_json))}")
                logger.info(
                    f"datasource_result length: {str(len(datasource_result))}")

                json_schema_file_path = cls.get_json_schema_file_path(
                    repository_path=repository_path, environment=environment)
                # Get the schema manifest
                msg = f"Loading manifest schema from {json_schema_file_path}"
                logger.info(msg)
                manifest = ManifestJson(json_schema_file_path)

                # Get the manifest file name
                manifest_json_file = cls.get_json_manifest_file_path(
                    "download", repository_path, datasource_title, schema_name, environment, alation_user_id)

                # Check if the datasource exists
                datasource = DataSource()
                datasource.check_datasource(
                    edc_alation_api_token, edc_alation_base_url, alation_datasource_id, datasource_title
                )

                # Get the schema structure
                manifest_dict = cls.get_schema_structure(
                    edc_alation_api_token, edc_alation_base_url, manifest, datasource_id, schema_id
                )

                # Write the file
                jsonString = json.dumps(manifest_dict, indent=4)
                jsonFile = open(manifest_json_file, "w", encoding='utf-8')
                jsonFile.write(jsonString)
                jsonFile.close()

                msg = "Wrote ManifestJson template file: " + manifest_json_file
                logger.info(msg)
                logger.info(
                    f"Validating the manifest file at {manifest_json_file} with schema"
                )

                # validate the manifest file
                metadata = manifest.validate_manifest(
                    manifest_json_file, json_schema_file_path)
                logger.info("Metadata File Validated")
                logger_singleton.force_flush()

                return manifest_json_file
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_column_name(schema_name, table_name, column):
        """
        Construct and return the full column name, including schema, table and column names.

        Args:
            schema_name (str): The name of the schema.
            table_name (str): The table object. Must have a 'name' attribute representing the name of the table.
            column (object): The column object. Must have a 'name' attribute representing the name of the column.

        Returns:
            str: The full column name in the format "schema_name.table.name.column.name".
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()
        with tracer.start_as_current_span("get_column_name"):

            try:

                column_name = getattr(column, 'name', column)
                full_column_name = f"{schema_name}.{table_name}.{column_name}"
                return full_column_name
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_table_structure(cls, edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_schema_id, unfetched_table, expected_table_fields, expected_column_fields):
        """
        Fetches the structure of a table, including its columns, based on the provided information.

        Args:
            alation_datasource_id (str): The Alation data source ID associated with the table.
            alation_schema_id (str): The Alation schema ID associated with the table.
            alation_headers (dict): The headers to be used for making API requests to Alation.
            edc_alation_base_url (str): The base URL for the Alation instance.
            unfetched_table (dict): A dictionary representing the unfetched table.
            expected_table_fields (list): A list of expected fields for the table.
            expected_column_fields (list): A list of expected fields for the columns in the table.

        Returns:
            dict: A dictionary representing the fetched table. The dictionary includes details about the table 
                and its columns. If the table has no columns, 'columns' key will have an empty list value.

        This function will:
            - Populate the fetched table dictionary with data from the unfetched table or with default values.
            - Retrieve all columns associated with the table from Alation and create a dictionary for each column.
            - Append each column dictionary to the 'columns' key in the fetched table dictionary.
        """

        if len(unfetched_table) >= len(expected_table_fields):
            fetched_table = {}
            for tf in expected_table_fields:
                # see if this field is already populated, otherwise use a default value
                if tf in unfetched_table:
                    fetched_table[tf] = unfetched_table[tf]
                else:
                    fetched_table[tf] = expected_table_fields[tf]

        # iterate through each column associated with this table and add a manifest template entry
        custom_field_dict = unfetched_table.get('custom_fields')
        alation_table_id = unfetched_table.get('id')
        columns_dict = cls.get_table_columns(
            edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_schema_id, alation_table_id)
        if columns_dict:
            fetched_table["columns"] = []
            # for each column associated with this table...
            for c in columns_dict:
                this_column_dict = {}
                for cf in expected_column_fields:
                    if cf in columns_dict[c]:
                        this_column_dict[cf] = columns_dict[c][cf]
                    else:
                        this_column_dict[cf] = expected_column_fields[cf]
                fetched_table["columns"].append(
                    this_column_dict)
            # iterate through each custom_field_dict
            if custom_field_dict:
                fetched_table["customfields"] = []
            # for each custon field associated with this table...
            for i in custom_field_dict:
                this_custom_flds_dict = {}
                this_custom_flds_dict[i['field_name']] = i['value']
                fetched_table["customfields"].append(
                    this_custom_flds_dict)

        return fetched_table

    @classmethod
    def get_schema_structure(cls, edc_alation_api_token, edc_alation_base_url, manifest, alation_datasource_id, alation_schema_id):
        """
        Retrieves the structure of a specific schema from Alation using the provided schema ID and manifest.

        Args:
            edc_alation_api_token (str): The API token for authenticating with the Alation instance.
            edc_alation_base_url (str): The base URL of the Alation instance.
            manifest (dict): The manifest defining the structure of the schema.
            alation_datasource_id (int): The ID of the Alation data source related to the schema.
            alation_schema_id (int): The ID of the Alation schema whose structure is to be retrieved.

        Raises:
            ValueError: If the response from the Alation API is not successful.

        Returns:
            tuple: A tuple containing the status code and a dictionary representing the structure of the schema.
        """

        try:
            logger_singleton = cdc_env_logging.LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME)
            logger = logger_singleton.get_logger()
            tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME)
            tracer = tracer_singleton.get_tracer()

            with tracer.start_as_current_span("get_schema_structure"):
                schema_result_json = None
                try:
                    schema_result, datasource_result = cls.get_schema(
                        edc_alation_api_token, edc_alation_base_url, alation_schema_id)
                    schema_result_json = schema_result.json()
                except requests.exceptions.RequestException as ex_r:
                    error_msg = "Error in requests: %s", str(ex_r)
                    exc_info = sys.exc_info()
                    logger_singleton.error_with_exception(error_msg, exc_info)
                    raise
                except Exception as ex_:
                    error_msg = "Error: %s", str(ex_)
                    exc_info = sys.exc_info()
                    logger_singleton.error_with_exception(error_msg, exc_info)
                    raise

                logger.info(f'Info for schema ID: {alation_schema_id}')
                found_schema = False
                schema_fields, expected_table_fields, expected_column_fields, required_table_fields = manifest.get_manifest_expected_fields()
                manifest_dict = {}
                manifest_dict['tables'] = []

                for schema in schema_result_json:
                    logger.info(f"schema_id: {str(schema['id'])}")
                    if schema['id'] == int(alation_schema_id):
                        found_schema = True

                        schema_name = schema['name']
                        logger.info(
                            f"Found the desired schema with name: {schema_name}")
                        logger.info(f"Structure length: {str(len(schema))}")
                        for field in schema_fields:
                            # Check if this field is already populated, otherwise use a default value
                            if field in schema:
                                manifest_dict[field] = schema[field]
                            else:
                                # Check if this field is in the list of custom fields
                                found_custom_field = False
                                for custom_field in schema['custom_fields']:
                                    formatted_field_name = field.lower().replace(" ", "")
                                    formatted_custom_field_name = custom_field['field_name'].lower().replace(
                                        " ", "")
                                    if formatted_field_name in formatted_custom_field_name:
                                        found_custom_field = True
                                        manifest_dict[field] = custom_field['value']
                                # Exceptions to the rule - Fields that need to be manually mapped
                                if not found_custom_field:
                                    # Enter the schema name in the identifier field
                                    if field == "identifier" and 'name' in schema:
                                        manifest_dict[field] = schema['name']
                                    elif field == "alationDatasourceID":
                                        manifest_dict[field] = alation_datasource_id
                                    elif field == "alationSchemaID":
                                        manifest_dict[field] = alation_schema_id
                                    else:
                                        manifest_dict[field] = schema_fields[field]

                        # Iterate through each table and add a manifest template entry
                        tables_dict = cls.get_schema_tables(
                            edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_schema_id)
                        if tables_dict:
                            # Determine the number of threads to use
                            num_threads = min(
                                NUM_THREADS_MAX, len(tables_dict))

                            # Using ThreadPoolExecutor
                            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                                futures = {}
                                for unfetched_table, table_info in tables_dict.items():
                                    future = executor.submit(cls.get_table_structure, edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_schema_id,
                                                             table_info, expected_table_fields, expected_column_fields)
                                    futures[unfetched_table] = future

                                for future in concurrent.futures.as_completed(futures.values()):
                                    manifest_dict["tables"].append(
                                        future.result())
                        else:
                            error_msg = "No tables found"
                            raise EdcAlationError(error_msg)

                if not found_schema:
                    error_msg = "Could not find the schema ID in the list of schemas for this data source"
                    raise EdcAlationError(error_msg)

                # Create a JSON structure containing the schema, tables, and columns
                return manifest_dict

        except Exception as ex:
            error_msg = str(ex)
            exc_info = sys.exc_info()
            logger_singleton.error_with_exception(error_msg, exc_info)
            raise EdcAlationError(error_msg) from ex

    @staticmethod
    def update_table_structure(edc_alation_api_token, edc_alation_base_url, alation_datasource_id, schema_name, table: alation_table.Table, force_submit, obj_custom_fields_endpoint, valid_editable_fields, table_name):
        """
        Updates the structure of a table in Alation.

        This method updates the table information, applies tags to the table, and
        updates the columns of the table. It uses Alation's custom fields API
        endpoint for updating the table and columns and applies tags using Alation's
        tags API endpoint.

        Parameters:
        alation_datasource_id (int): The ID of the Alation data source where the table resides.
        schema_name (str): The name of the schema where the table resides.
        edc_alation_edc_alation_edc_alation_api_access_token (str): The API access token for Alation.
        edc_alation_base_url (str): The base URL for Alation's API.
        unposted_table (Table): The table object that contains the updated structure.

        Returns:
        int: HTTP status code of the operation. 200 indicates success.
        str: Status message of the operation. "OK" indicates success.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()
        with tracer.start_as_current_span("upload_schema_manifest"):

            try:

                if table_name is None:
                    raise ValueError('table_name cannot be None.')

                id_finder_endpoint = IdFinderEndpoint(
                    edc_alation_api_token, edc_alation_base_url)
                tags_endpoint = TagsEndpoint(
                    edc_alation_api_token, edc_alation_base_url)

                if schema_name == 'object_name_is_missing' or schema_name == 'object name is missing':
                    raise ValueError('Invalid schema_name value.')

                # encode the schema
                if '.' in schema_name and ENCODE_PERIOD:
                    encoded_schema_name = f"\"{schema_name}\""
                else:
                    encoded_schema_name = schema_name

                # encode the table
                special_chars = set('!"#$%&\\\'()*+,-./:;<=>?@[\\]^_`{}~')

                if any(char in special_chars for char in table_name) and ENCODE_PERIOD:
                    encoded_table_name = f"\"{table_name}\""
                else:
                    encoded_table_name = table_name

                key = f"{encoded_schema_name}.{encoded_table_name}"
                # Update the table
                # Should only be one - ensure force_submit
                response_content = obj_custom_fields_endpoint.update(
                    edc_alation_api_token, edc_alation_base_url, "table", alation_datasource_id, key, table, force_submit=force_submit, valid_editable_fields=valid_editable_fields)

                last_result = response_content
                logger.info(f"response_content: {response_content}")

                # Update the tags
                # Encode ignoring ENCODE_PERIOD
                # encode the schema
                if '.' in schema_name:
                    encoded_schema_name = f"\"{schema_name}\""
                else:
                    encoded_schema_name = schema_name

                if '.' in table_name:
                    encoded_table_name = f"\"{table_name}\""
                else:
                    encoded_table_name = table_name

                table_key = f"{alation_datasource_id}.{encoded_schema_name}.{encoded_table_name}"

                # Apply tags to the table
                if isinstance(table, alation_table.Table):
                    if table.tags is not None:
                        table_id = id_finder_endpoint.find(
                            'table', table_key)
                        for table_tag in table.tags:
                            tags_endpoint.apply(
                                'table', table_id, table_tag)

                    from data_ecosystem_services.alation_service.db_column import Column
                    # Update the columns to convert string to objects if necessary
                    columns_dict = table.columns
                else:
                    columns_dict = table

                # # Update the columns
                # if columns_dict is not None:

                #     # Using ThreadPoolExecutor
                #     num_threads = min(NUM_THREADS_MAX, len(columns_dict))

                #     if '.' in schema_name and ENCODE_PERIOD:
                #         encoded_schema_name = f"\"{schema_name}\""
                #     else:
                #         encoded_schema_name = schema_name

                #     special_chars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{}~')

                #     if any(char in special_chars for char in table_name) and ENCODE_PERIOD:
                #         encoded_table_name = f"\"{table_name}\""
                #     else:
                #         encoded_table_name = table_name

                #     with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                #         last_future_result = ""
                #         futures = []
                #         total_items = len(columns_dict.items())
                #         special_chars = set(
                #             '!"#$%&\\\'()*+,-./:;<=>?@[\\]^_`{}~')

                #         for idx, (key, value) in enumerate(columns_dict.items()):
                #             # Set force_submit to True on the last item
                #             force_submit = (idx == total_items - 1)
                #             if any(char in special_chars for char in key) and ENCODE_PERIOD:
                #                 encoded_column_name = f"\"{key}\""
                #             else:
                #                 encoded_column_name = key

                #             future = executor.submit(obj_custom_fields_endpoint.update, edc_alation_api_token, edc_alation_base_url, "attribute",
                #                                      alation_datasource_id,
                #                                      f"{encoded_schema_name}.{encoded_table_name}.{encoded_column_name}",
                #                                      value, force_submit=force_submit, valid_editable_fields=valid_editable_fields)
                #             futures.append(future)

                #         # Wait for all futures to complete
                #         concurrent.futures.wait(futures)

                #         # Retrieve the result of the last future
                #         if futures:
                #             last_future_result = futures[-1].result()
                #         else:
                #             last_future_result = "No return value from last update call"

                #         last_result = str(last_result) + \
                #             str(last_future_result)

                # else:
                #     warning_msg = f"No columns supplied to update for table: {table_name}"
                #     logger.warning(warning_msg)
                #     last_result = str(last_result) + warning_msg

                return last_result

            except Exception as ex:
                error_msg = f"Error: {str(ex)}",
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def upload_schema_manifest_json_file(cls, metadata_json_data, config):
        """
        Uploads a schema manifest to Alation.

        Args:
            metadata_json_data (dict): Contains metadata information such as the Alation Schema ID.
            config (dict): Configuration data with the following keys:
                - edc_alation_base_url (str): The base URL of the Alation instance.
                - yyyy (str): Year component for manifest file generation.
                - mm (str): Month component for manifest file generation.
                - dd (str): Day component for manifest file generation.
                - repository_path (str): Path to the repository for manifest file.
                - environment (str): The current environment in use.
                - edc_json_schema_location (str): The location of EDC schema.
                - edc_alation_user_id (str): The user ID for Alation API.

        Returns:
            manifest_dict (dict): A dictionary with the key "result" set to "success" if the operation completes successfully.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("upload_schema_manifest"):
            try:

                # Get the configuration data
                edc_alation_base_url = config.get("edc_alation_base_url")
                # Format as a 24-hour time string
                repository_path = config.get("repository_path")
                environment = config.get("environment")
                alation_user_id = config.get("edc_alation_user_id")

                # Get the Alation Schema ID form the json
                alation_schema_id = metadata_json_data["alationSchemaID"]

                logger.info(f"alation_user_id:{alation_user_id}")

                # Get the API access token
                token_endpoint = TokenEndpoint(edc_alation_base_url)
                status_code, edc_alation_api_token, alation_refresh_token = token_endpoint.get_api_token_from_config(
                    config)
                logger.info(
                    f"get_api_token_from_config:status_code:{status_code}")
                msg = f"edc_alation_api_token length:{str(len(edc_alation_api_token))}"
                logger.info(msg)

                if len(edc_alation_api_token.strip()) == 0:
                    msg = "Alation API Access Token is not set"
                    raise ValueError(msg)

                # Get the schema and datasource information
                schema_results, datasource_results = cls.get_schema(
                    edc_alation_api_token, edc_alation_base_url, alation_schema_id
                )

                # Get the schema and datasource information
                schema_result_json = schema_results.json()
                schema_name = schema_result_json[0].get("name")
                datasource_title = datasource_results.get("title")
                alation_datasource_id = datasource_results.get("id")

                # Get the json schema file path
                json_schema_file_path = cls.get_json_schema_file_path(
                    repository_path, environment)
                table = alation_table.Table(None, json_schema_file_path)

                # Get expected table structure from Excel structure file
                df_tables = table.get_tables_for_schema(config,
                                                        alation_datasource_id, alation_schema_id)

                # Get the valid editable fields
                valid_editable_fields = table.get_valid_editable_fields_from_schema_xlsx(
                    df_tables)

                # Get the manifest file name
                manifest_json_file = cls.get_json_manifest_file_path(
                    "upload", repository_path, datasource_title, schema_name, environment, alation_user_id)

                # Write the manifest file
                with open(manifest_json_file, "w", encoding='utf-8') as f:
                    json.dump(metadata_json_data, f)

                # Validate the manifest file
                msg = 'Validating the manifest file at {0} with schema'.format(
                    manifest_json_file)
                logger.info(msg)

                manifest = ManifestJson(json_schema_file_path)
                metadata = manifest.validate_manifest(
                    manifest_json_file, json_schema_file_path)
                logger.info(
                    f"Metadata File Validated file of length {str(len(metadata))}")

                # Update based on ManifestJson file
                if token_endpoint.validate_refresh_token(alation_user_id, alation_refresh_token) is not None:

                    custom_fields_endpoint = CustomFieldsEndpoint()
                    logger.info(
                        'Created custom fields endpoint for updating custom fields via API')

                    tags_endpoint = TagsEndpoint(
                        edc_alation_api_token, edc_alation_base_url)
                    logger.info(
                        'Created tags endpoint for updating tags via API')

                    id_finder_endpoint = IdFinderEndpoint(
                        edc_alation_api_token, edc_alation_base_url)

                    # encode key
                    # always encode schema name regardless of ENCODE_PERIOD
                    if '.' in schema_name:
                        encoded_schema_name = f"\"{schema_name}\""
                    else:
                        encoded_schema_name = schema_name

                    # Update the schema
                    logger.info(
                        'Created id finder for getting detailed information on Alation objects')
                    logger.info('Updating the schema fields for data source {0} and schema {1}'.format(
                        alation_datasource_id, schema_name))

                    schema = manifest.get_schema_data()
                    response_content = custom_fields_endpoint.update(edc_alation_api_token, edc_alation_base_url,
                                                                     "schema", alation_datasource_id, encoded_schema_name, schema, True, valid_editable_fields=valid_editable_fields)
                    logger.info("response_content: " + str(response_content))
                    schema_key = str(alation_datasource_id) + \
                        "." + encoded_schema_name
                    schema_id = id_finder_endpoint.find('schema', schema_key)
                    for tag in manifest.tags:
                        tags_endpoint.apply('schema', schema_id, tag)

                    # Update the tables
                    tables_dict = manifest.get_tables_data()
                    if tables_dict:
                        total_items = len(tables_dict.items())
                        # reinit endpoint
                        obj_custom_fields_endpoint = CustomFieldsEndpoint()

                        for idx, (table_name, value) in enumerate(tables_dict.items()):
                            # Set force_submit to True on the last item
                            force_submit = (idx == total_items - 1)

                            table_result = cls.update_table_structure(edc_alation_api_token,
                                                                      edc_alation_base_url, alation_datasource_id, schema_name,
                                                                      value, force_submit=force_submit, obj_custom_fields_endpoint=obj_custom_fields_endpoint, valid_editable_fields=valid_editable_fields, table_name=table_name)
                            logger.info("table_result: " + str(table_result))
                        # Commented out the threading because complexity not worth it
                        # compared to batching updates in sets of 50
                        # and limiting updates to differences

                        # num_threads = min(NUM_THREADS_MAX, len(tables_dict))

                        # Using ThreadPoolExecutor
                        # with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                        #    futures = []
                        #    items = list(tables_dict.items())
                        #    total_items = len(items)

                            # for idx, (key, value) in enumerate(items):
                            # Set force_submit to True on the last item

                            #    future = executor.submit(cls.update_table_structure, edc_alation_api_token,
                            #                             edc_alation_base_url, alation_datasource_id, schema_name,
                            #                             value, force_submit=force_submit)
                            #    futures.append(future)

                        # Wait for all futures to complete
                        # concurrent.futures.wait(futures)
                        return tables_dict

                    else:
                        error_msg = "No tables found"
                        raise EdcAlationError(error_msg)
                else:
                    error_msg = "Refresh token is not valid"
                    raise EdcAlationError(error_msg)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def upload_schema_manifest_excel_file(cls, manifest_excel_file_path, config, json_schema_file_path):
        """
        Uploads a schema manifest to Alation.

        Args:
            metadata_excel_data (dict): Contains metadata information such as the Alation Schema ID.
            config (dict): Configuration data with the following keys:
                - edc_alation_base_url (str): The base URL of the Alation instance.
                - yyyy (str): Year component for manifest file generation.
                - mm (str): Month component for manifest file generation.
                - dd (str): Day component for manifest file generation.
                - repository_path (str): Path to the repository for manifest file.
                - environment (str): The current environment in use.
                - edc_json_schema_location (str): The location of EDC schema.
                - edc_alation_user_id (str): The user ID for Alation API.

        Returns:
            manifest_dict (dict): A dictionary with the key "result" set to "success" if the operation completes successfully.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("upload_schema_manifest"):
            try:

                # Get the configuration data
                edc_alation_base_url = config.get("edc_alation_base_url")
                # Format as a 24-hour time string
                repository_path = config.get("repository_path")
                environment = config.get("environment")
                alation_user_id = config.get("edc_alation_user_id")
                json_schema_file_path = cls.get_json_schema_file_path(
                    repository_path, environment)
                logger.info(f"alation_user_id:{alation_user_id}")

                # Get the API access token
                token_endpoint = TokenEndpoint(edc_alation_base_url)
                status_code, edc_alation_api_token, alation_refresh_token = token_endpoint.get_api_token_from_config(
                    config)
                logger.info(
                    f"get_api_token_from_config:status_code:{status_code}")
                msg = f"edc_alation_api_token length:{str(len(edc_alation_api_token))}"
                logger.info(msg)

                if len(edc_alation_api_token.strip()) == 0:
                    msg = "Alation API Access Token is not set"
                    raise ValueError(msg)

                manifest_excel = alation_manifest_excel.ManifestExcel()
                df_tables = manifest_excel.read_manifest_excel_file_tables_worksheet(
                    manifest_excel_file_path)
                alation_schema_id = df_tables['schema_id'][0]
                logger.info(f"alation_schema_id:{alation_schema_id}")

                # Get the schema and datasource information
                schema_results, datasource_results = cls.get_schema(
                    edc_alation_api_token, edc_alation_base_url, alation_schema_id
                )

                schema_result_json = schema_results.json()
                schema_name = schema_result_json[0].get("name")
                alation_datasource_id = datasource_results.get("id")

                table = alation_table.Table(None, json_schema_file_path)

                # Get expected table structure from Excel structure file
                df_tables_expected = table.get_tables_for_schema(config,
                                                                 alation_datasource_id, alation_schema_id)

                # Get the valid editable fields
                valid_editable_fields = table.get_valid_editable_fields_from_schema_xlsx(
                    df_tables_expected)

                # Update based on ManifestJson file
                if token_endpoint.validate_refresh_token(alation_user_id, alation_refresh_token) is not None:

                    custom_fields_endpoint = CustomFieldsEndpoint()
                    logger.info(
                        'Created custom fields endpoint for updating custom fields via API')

                    tags_endpoint = TagsEndpoint(
                        edc_alation_api_token, edc_alation_base_url)
                    logger.info(
                        'Created tags endpoint for updating tags via API')

                    id_finder_endpoint = IdFinderEndpoint(
                        edc_alation_api_token, edc_alation_base_url)

                    # encode key
                    # always encode schema name regardless of ENCODE_PERIOD
                    if '.' in schema_name:
                        encoded_schema_name = f"\"{schema_name}\""
                    else:
                        encoded_schema_name = schema_name

                    # Update the schema
                    logger.info(
                        'Created id finder for getting detailed information on Alation objects')
                    logger.info(
                        f"Updating the schema fields for data source {alation_datasource_id} and schema {schema_name}")

                    # TODO Update schema info when the schema tab is implemented
                    # response_content = custom_fields_endpoint.update(edc_alation_api_token, edc_alation_base_url,
                    #                                                  "schema", alation_datasource_id, encoded_schema_name, schema, True, valid_editable_fields=valid_editable_fields)
                    # logger.info("response_content: " + str(response_content))
                    # TODO Update the schema tags
                    # schema_key = str(alation_datasource_id) + \
                    #     "." + encoded_schema_name
                    # schema_id = id_finder_endpoint.find('schema', schema_key)
                    # for tag in manifest.tags:
                    #    tags_endpoint.apply('schema', schema_id, tag)

                    # Convert df_tables to a dictionary with 'table_name' as the key
                    tables_dict = df_tables.set_index(
                        'name').to_dict(orient='index')

                    if tables_dict:
                        total_items = len(tables_dict.items())
                        # reinit endpoint
                        obj_custom_fields_endpoint = CustomFieldsEndpoint()

                        for idx, (key, table) in enumerate(tables_dict.items()):
                            # Set force_submit to True on the last item
                            force_submit = idx == total_items - 1

                            table_name = key
                            table_result = cls.update_table_structure(edc_alation_api_token,
                                                                      edc_alation_base_url, alation_datasource_id, schema_name,
                                                                      table, force_submit=force_submit, obj_custom_fields_endpoint=obj_custom_fields_endpoint, valid_editable_fields=valid_editable_fields, table_name=table_name)
                            logger.info("table_result: " + str(table_result))

                        # Commented out the threading because complexity not worth it
                        # compared to batching updates in sets of 50
                        # and limiting updates to differences

                        # num_threads = min(NUM_THREADS_MAX, len(tables_dict))

                        # Using ThreadPoolExecutor
                        # with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                        #    futures = []
                        #    items = list(tables_dict.items())
                        #    total_items = len(items)

                        # for idx, (key, value) in enumerate(items):
                        # Set force_submit to True on the last item

                        #    future = executor.submit(cls.update_table_structure, edc_alation_api_token,
                        #                             edc_alation_base_url, alation_datasource_id, schema_name,
                        #                             value, force_submit=force_submit)
                        #    futures.append(future)

                        # Wait for all futures to complete
                        # concurrent.futures.wait(futures)
                        return tables_dict

                    else:
                        error_msg = "No tables found"
                        raise EdcAlationError(error_msg)
                else:
                    error_msg = "Refresh token is not valid"
                    raise EdcAlationError(error_msg)
            except Exception as ex:
                error_msg = f"Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
