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
import numpy as np


from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging
)

import data_ecosystem_services.cdc_tech_environment_service.environment_file as cdc_env_file
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


class Table:
    """
    Represents a table object.

    """

    def __init__(self, table_json, schema_file_path):
        """
        Initializes a Table object using the provided table JSON.

        Args:
            table_json (dict): The JSON data representing the table.

        Raises:
            Exception: If an error occurs during initialization.

        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("__init__"):

            try:

                self.schema_file_path = schema_file_path

                if table_json is None:
                    return

                manifest = ManifestJson(schema_file_path)

                # get the expected fields from the manifest
                schema_fields, expected_table_fields, expected_column_fields, required_table_fields = manifest.get_manifest_expected_fields()

                msg = "Schema fields length: " + str(len(schema_fields))
                logger.info(msg)
                msg = "Expected table fields length: " + \
                    str(len(expected_column_fields))
                logger.info(msg)

                # add specified tables fields to the table object and update if necessary
                for key in expected_table_fields:
                    if key in table_json:
                        setattr(self, key, table_json[key])

                missing_keys = [
                    key for key in required_table_fields if not hasattr(self, key)]

                if missing_keys:
                    logger.error(f"Missing keys: {missing_keys}")

                # get the extra description fields from the table JSON
                self.extra_description_fields = self.get_table_extra_description_fields(
                    table_json)

                self.name = table_json.get('name')
                self.title = table_json.get('title')
                self.description = self.format_description(table_json)

                tags = table_json.get('tags')
                if tags is not None:
                    self.tags = tags
                else:
                    self.tags = []
                columns_json = table_json.get('columns')

                if columns_json is not None:
                    # self.columns = list(
                    #     map(lambda c: Column(c, schema_file_path), columns_json))
                    self.columns = {column.name: column for column in map(
                        lambda c: Column(c, self.schema_file_path), columns_json)}

                else:
                    self.columns = None
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_alation_data(self):
        """
        Retrieves the title and description from the instance.

        This function checks the 'title' and 'description' attributes of the instance and returns a dictionary that includes 
        'title' and 'description' keys, each with their respective values, only if the values are not None. 
        It includes keys whose values are empty strings.

        Returns:
            dict: A dictionary with 'title' and 'description' keys. The dictionary will not include keys whose values are None.
            If both 'title' and 'description' are None, an empty dictionary is returned.
        """
        return {k: v for k, v in {
            'title': self.title,
            'description': self.description
        }.items() if v is not None}

    def get_valueset_for_tables_sql_xlsx(self, valueset_name):
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_valueset_for_tables_sql_xlsx"):

            # Change the current working directory to the project root directory
            os.chdir(project_root)
            # Get the file utility object
            obj_file = cdc_env_file.EnvironmentFile()

            # Get the manifest file
            schema_file = self.schema_file_path
            directory = os.path.dirname(schema_file) + "/"
            directory = obj_file.convert_to_current_os_dir(directory)
            schema_file_valuesets = directory + "excel_manifest_schema_valuesets.xlsx"
            file_exists = obj_file.file_exists(
                True, schema_file_valuesets, None)
            logger.info(f"file_exists: {file_exists}")
            df_fields_excel_table = pd.read_excel(
                schema_file_valuesets, valueset_name)
            return df_fields_excel_table, schema_file

    def get_schema_for_tables_sql_xlsx_path(self):
        """
        Get the file path of the 'excel_manifest_schema_for_tables_sql.xlsx' file based on the provided schema_file_path.

        This function takes no arguments and utilizes the 'self.schema_file_path' attribute to extract the directory path
        where the 'excel_manifest_schema_for_tables_sql.xlsx' file is expected to be located. It then constructs the complete file path
        by joining the directory path with the filename. The constructed file path is returned.

        Returns:
            str: The complete file path of the 'excel_manifest_schema_for_tables_sql.xlsx' file based on the provided schema_file_path.

        Note:
            This function assumes the existence of the 'self.schema_file_path' attribute representing the file path of the source schema.


        """
        # Get the directory part of the file path
        directory_path = os.path.dirname(self.schema_file_path)

        schema_xls_file = "excel_manifest_schema_for_tables_sql.xlsx"

        # Join the directory path and the file name
        schema_xls_file_path = os.path.join(
            directory_path, schema_xls_file)

        return schema_xls_file_path

    def get_schema_for_tables_sql_xlsx(self):
        """
        Reads an Excel file containing a schema for SQL tables from a specific location in the file system.

        The function first changes the current working directory to the project root directory, and then creates 
        an instance of the EnvironmentFile class. It constructs a path to the file location based on the current 
        environment and checks whether the file exists. The function reads the Excel file into a pandas DataFrame 
        and returns the DataFrame and the file path.

        The function raises an AssertionError if the file does not exist.

        Returns:
            tuple: A tuple containing a pandas DataFrame representing the content of the Excel file and the path 
            to the file.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_schema_for_tables_sql_xlsx"):

            # Get the file utility object
            obj_file = cdc_env_file.EnvironmentFile()

            # Get the excel schema file
            excel_schema_file_path = self.get_schema_for_tables_sql_xlsx_path()
            file_exists = obj_file.file_exists(
                True, excel_schema_file_path, None)
            logger.info(f"file_exists: {file_exists}")
            df_fields_excel_table = pd.read_excel(excel_schema_file_path)
            return df_fields_excel_table, excel_schema_file_path

    def get_valid_required_fields_from_schema_xlsx(self, df_tables):
        """
        Retrieve a list of valid required columns from the Excel schema DataFrame based on the provided table DataFrame.

        Parameters:
            df_fields_excel_schema (pd.DataFrame): A pandas DataFrame representing the Excel schema with column information.
            df_tables (pd.DataFrame): A pandas DataFrame representing the table for which valid required columns are to be determined.

        Returns:
            list: A list of column names from the Excel schema DataFrame that are marked as 'allow-edits' and exist in the table DataFrame.
        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_valid_html_columns_from_schema_xlsx"):

            # Get expected table structure from Excel structure file
            df_fields_excel_schema, schema_file = self.get_schema_for_tables_sql_xlsx()

            # Column that stores flag indicating if column contains HTML
            column_name_flagging_required = 'excel_is_required'
            logger.info(
                f"column_name_flagging_required: {column_name_flagging_required}")

            if column_name_flagging_required in df_fields_excel_schema.columns:
                # html columns
                df_required_fields_excel_schema = df_fields_excel_schema[
                    df_fields_excel_schema[column_name_flagging_required] == 'required']
                required_columns = df_required_fields_excel_schema['field_name'].tolist(
                )
            else:
                # Assuming you have a DataFrame named 'df_fields_excel_schema'
                # To list all columns of the DataFrame 'df_fields_excel_schema'
                column_list = df_fields_excel_schema.columns.tolist()
                logger.info(str(column_list))
                logger.warning(
                    f"No {column_name_flagging_required} column in Excel schema file")
                required_columns = []

            # Get a list of columns that exist in both df_tables and l
            table_column_names = df_tables.columns.tolist()
            valid_required_fields = [
                col for col in required_columns if col in table_column_names]

            return valid_required_fields

    def get_valid_date_fields_from_schema_xlsx(self, df_fields_excel_schema, df_tables):
        """
        Retrieve a list of valid date columns from the Excel schema DataFrame based on the provided table DataFrame.

        This function extracts column names from the Excel schema DataFrame (df_fields_excel_schema) that are marked with
        'DATE' as the field type ('field_type_alation'). It then checks if these columns exist in the table DataFrame
        (df_tables). If a column is present in both the Excel schema and the table, it is considered a valid date column.

        Additionally, if the 'description' column is not marked as an date column in the schema but is present in the table,
        it is also included in the list of valid date columns.

        Parameters:
            df_fields_excel_schema (pd.DataFrame): A pandas DataFrame representing the Excel schema with column information.
            df_tables (pd.DataFrame): A pandas DataFrame representing the table for which valid date columns are to be determined.

        Returns:
            list: A list of column names from the Excel schema DataFrame that are marked as 'DATE' and exist in the table DataFrame,
                including the 'description' column if present in the table but not explicitly marked as an date column in the schema.
        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_valid_date_columns_from_schema_xlsx"):
            # Column that stores flag indicating if column contains date
            column_name_flagging_date = 'field_type_alation'
            logger.info(
                f"column_name_flagging_date: {column_name_flagging_date}")

            if column_name_flagging_date in df_fields_excel_schema.columns:
                # date columns
                df_date_fields_excel_schema = df_fields_excel_schema[
                    df_fields_excel_schema[column_name_flagging_date] == 'DATE']
                date_columns = df_date_fields_excel_schema['field_name'].tolist(
                )
            else:
                # Assuming you have a DataFrame named 'df_fields_excel_schema'
                # To list all columns of the DataFrame 'df_fields_excel_schema'
                column_list = df_fields_excel_schema.columns.tolist()
                logger.info(str(column_list))
                logger.warning(
                    f"No {column_name_flagging_date} column in Excel schema file")
                date_columns = []

            # Get a list of columns that exist in both df_tables and date_columns
            table_column_names = df_tables.columns.tolist()
            valid_date_columns = [
                col for col in date_columns if col in table_column_names]

            return valid_date_columns

    def get_valid_object_set_columns_from_schema_xlsx(self, df_fields_excel_schema, df_tables):
        """
        Retrieve a list of valid object_set columns from the Excel schema DataFrame based on the provided table DataFrame.

        This function extracts column names from the Excel schema DataFrame (df_fields_excel_schema) that are marked with
        'OBJECT_SET' as the field type ('field_type_alation'). It then checks if these columns exist in the table DataFrame
        (df_tables). If a column is present in both the Excel schema and the table, it is considered a valid object_set column.

        Additionally, if the 'description' column is not marked as an object_set column in the schema but is present in the table,
        it is also included in the list of valid object_set columns.

        Parameters:
            df_fields_excel_schema (pd.DataFrame): A pandas DataFrame representing the Excel schema with column information.
            df_tables (pd.DataFrame): A pandas DataFrame representing the table for which valid object_set columns are to be determined.

        Returns:
            list: A list of column names from the Excel schema DataFrame that are marked as 'OBJECT_SET' and exist in the table DataFrame,
                including the 'description' column if present in the table but not explicitly marked as an object_set column in the schema.
        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_valid_object_set_columns_from_schema_xlsx"):
            # Column that stores flag indicating if column contains object_set
            column_name_flagging_object_set = 'field_type_alation'
            logger.info(
                f"column_name_flagging_object_set: {column_name_flagging_object_set}")

            if column_name_flagging_object_set in df_fields_excel_schema.columns:
                # object_set columns
                df_object_set_fields_excel_schema = df_fields_excel_schema[
                    df_fields_excel_schema[column_name_flagging_object_set] == 'OBJECT_SET']
                object_set_columns = df_object_set_fields_excel_schema['field_name'].tolist(
                )
            else:
                # Assuming you have a DataFrame named 'df_fields_excel_schema'
                # To list all columns of the DataFrame 'df_fields_excel_schema'
                column_list = df_fields_excel_schema.columns.tolist()
                logger.info(str(column_list))
                logger.warning(
                    f"No {column_name_flagging_object_set} column in Excel schema file")
                object_set_columns = []

            # Get a list of columns that exist in both df_tables and object_set_columns
            table_column_names = df_tables.columns.tolist()
            valid_object_set_columns = [
                col for col in object_set_columns if col in table_column_names]

            return valid_object_set_columns

    def get_valid_editable_fields_from_schema_xlsx(self, df_tables):
        """
        Retrieve a list of valid editable columns from the Excel schema DataFrame based on the provided table DataFrame.

        Parameters:
            df_fields_excel_schema (pd.DataFrame): A pandas DataFrame representing the Excel schema with column information.
            df_tables (pd.DataFrame): A pandas DataFrame representing the table for which valid editable columns are to be determined.

        Returns:
            list: A list of column names from the Excel schema DataFrame that are marked as 'allow-edits' and exist in the table DataFrame.
        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_valid_editable_fields_from_schema_xlsx"):

            # Get expected table structure from Excel structure file
            df_fields_excel_schema, schema_file = self.get_schema_for_tables_sql_xlsx()

            # Column that stores flag indicating if column contains HTML
            column_name_flagging_editable = 'excel_read_only'
            logger.info(
                f"column_name_flagging_editable: {column_name_flagging_editable}")

            if column_name_flagging_editable in df_fields_excel_schema.columns:
                # html columns
                df_editable_fields_excel_schema = df_fields_excel_schema[
                    df_fields_excel_schema[column_name_flagging_editable] == 'allow-edits']
                editable_columns = df_editable_fields_excel_schema['field_name'].tolist(
                )
            else:
                # Assuming you have a DataFrame named 'df_fields_excel_schema'
                # To list all columns of the DataFrame 'df_fields_excel_schema'
                column_list = df_fields_excel_schema.columns.tolist()
                logger.info(str(column_list))
                logger.warning(
                    f"No {column_name_flagging_editable} column in Excel schema file")
                editable_columns = []

            # Get a list of columns that exist in both df_tables and l
            table_column_names = df_tables.columns.tolist()
            valid_editable_fields = [
                col for col in editable_columns if col in table_column_names]

            return valid_editable_fields

    def get_valid_html_columns_from_schema_xlsx(self, df_fields_excel_schema, df_tables):
        """
        Retrieve a list of valid HTML columns from the Excel schema DataFrame based on the provided table DataFrame.

        This function extracts column names from the Excel schema DataFrame (df_fields_excel_schema) that are marked with
        'RICH_TEXT' as the field type ('field_type_alation'). It then checks if these columns exist in the table DataFrame
        (df_tables). If a column is present in both the Excel schema and the table, it is considered a valid HTML column.

        Additionally, if the 'description' column is not marked as an HTML column in the schema but is present in the table,
        it is also included in the list of valid HTML columns.

        Parameters:
            df_fields_excel_schema (pd.DataFrame): A pandas DataFrame representing the Excel schema with column information.
            df_tables (pd.DataFrame): A pandas DataFrame representing the table for which valid HTML columns are to be determined.

        Returns:
            list: A list of column names from the Excel schema DataFrame that are marked as 'RICH_TEXT' and exist in the table DataFrame,
                including the 'description' column if present in the table but not explicitly marked as an HTML column in the schema.
        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_valid_html_columns_from_schema_xlsx"):
            # Column that stores flag indicating if column contains HTML
            column_name_flagging_html = 'field_type_alation'
            logger.info(
                f"column_name_flagging_html: {column_name_flagging_html}")

            if column_name_flagging_html in df_fields_excel_schema.columns:
                # HTML columns
                df_html_fields_excel_schema = df_fields_excel_schema[
                    df_fields_excel_schema[column_name_flagging_html] == 'RICH_TEXT']
                html_columns = df_html_fields_excel_schema['field_name'].tolist(
                )
            else:
                # Assuming you have a DataFrame named 'df_fields_excel_schema'
                # To list all columns of the DataFrame 'df_fields_excel_schema'
                column_list = df_fields_excel_schema.columns.tolist()
                logger.info(str(column_list))
                logger.warning(
                    f"No {column_name_flagging_html} column in Excel schema file")
                html_columns = []

            # Get a list of columns that exist in both df_tables and html_columns
            table_column_names = df_tables.columns.tolist()
            valid_html_columns = [
                col for col in html_columns if col in table_column_names]

            if "description" not in valid_html_columns:
                valid_html_columns.append("description")

            return valid_html_columns

    def get_tables_for_schema(self, config, alation_datasource_id, alation_schema_id):
        """
        Retrieve tables associated with a specific schema from Alation using the provided configuration and authentication.

        This function queries Alation's integration API to retrieve tables associated with the given schema (alation_schema_id)
        from the specified datasource (alation_datasource_id). It requires valid configuration parameters (config) to access the Alation API.

        Parameters:
            config (dict): A dictionary containing the required configuration parameters to access the Alation API. It should include:
                        - 'edc_alation_base_url': The base URL of the Alation instance.
            alation_datasource_id (int): The ID of the datasource in Alation that contains the desired schema.
            alation_schema_id (int): The ID of the schema in Alation for which tables are to be retrieved.

        Returns:
            pandas.DataFrame: A pandas DataFrame containing the tables associated with the specified schema. The DataFrame will be
                            structured with each table as a row and columns representing various properties of the tables, including
                            custom fields if any are defined.

        Note:
            The function requires the 'requests' library and 'pandas' library for API calls and data processing, respectively.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the API call to Alation.

        Example:
            config = {
                'edc_alation_base_url': 'https://your_alation_instance.com'
            }
            datasource_id = 123
            schema_id = 456
            tables_dataframe = get_tables_for_schema(config, datasource_id, schema_id)
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_tables_for_schema"):

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
            # api for tables
            api = "/integration/v2/table/"

            limit = 500
            skip = 0

            # Create a dictionary to hold the parameters
            params = {}
            params['limit'] = limit
            params['skip'] = skip
            params['schema_id'] = alation_schema_id
            params['ds_id'] = alation_datasource_id

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

    @staticmethod
    def wrap_in_brackets(text):
        """
        Wrap a given string in brackets if they are not already present.

        Parameters:
            text (str): The input string to be wrapped in brackets.

        Returns:
            str: The input string wrapped in brackets, or the original string if it already has brackets.

        Example:
            # Test cases
            text1 = "Hello, world!"
            text2 = "(Welcome to the party)"
            text3 = "Python is awesome"

            print(wrap_in_brackets(text1))  # Output: "(Hello, world!)"
            print(wrap_in_brackets(text2))  # Output: "(Welcome to the party)"
            print(wrap_in_brackets(text3))  # Output: "(Python is awesome)"

        Note:
            This method checks if the input string starts with an opening bracket '(' and ends with a closing bracket ')'.
            If the brackets are not present, the method wraps the string in brackets using string formatting (f'({text})').
            If the string is already wrapped in brackets, the method returns the original string as it is.
        """
        if text.startswith('[') and text.endswith(']'):
            return text  # The string is already wrapped in brackets, return as it is
        else:
            return f'[{text}]'  # Wrap the string in brackets and return

    def get_tables_for_schema_for_excel(self, config, alation_datasource_id, alation_schema_id):
        """
        This function fetches tables for a specified schema from Alation for excel processing.
        The function first gets an API token from the config using the token_endpoint helper. 
        It then constructs the necessary parameters for a GET request to the Alation API, 
        where it fetches the tables for the given schema. The function then processes the 
        API response to expand the JSON, transform it into a dataframe and match column 
        names with a predefined schema from an Excel source. After this, the data is sorted 
        by the order defined in the Excel schema.

        Args:
            config (dict): A configuration dictionary containing necessary API information.
            alation_datasource_id (int): The Alation id of the datasource to fetch tables from.
            alation_schema_id (int): The Alation id of the schema to fetch tables from.

        Returns:
            None. The function prints out the sorted dataframe containing the tables.
            For future use, this function could be modified to return the dataframe.

        Raises:
            AssertionError: An error occurred if the status code from the token endpoint is not 200.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_tables_for_schema_for_excel"):

            # Get db tables from Alation for the specfied db schema
            df_tables = self.get_tables_for_schema(
                config, alation_datasource_id, alation_schema_id)

            # Get expected table structure from Excel structure file
            df_fields_excel_schema, excel_schema_file = self.get_schema_for_tables_sql_xlsx()

            # Get valid object_set columns from expected table structure
            valid_object_set_columns = self.get_valid_object_set_columns_from_schema_xlsx(
                df_fields_excel_schema, df_tables)

            # Convert valid object_set columns
            for column in valid_object_set_columns:
                # for each row in the column
                for idx in df_tables.index:
                    # Get the value at the current cell
                    cell_value = df_tables.loc[idx, column]
                    try:
                        # Try to parse it as HTML
                        if cell_value is None:
                            cell_value = ''

                        if not isinstance(cell_value, (list, np.ndarray)):
                            if pd.isna(cell_value):
                                cell_value = ''

                        if isinstance(cell_value, str):
                            cell_value = self.wrap_in_brackets(cell_value)
                            # Parse the JSON string into a Python dictionary
                            parsed_data = json.loads(cell_value)
                        else:
                            parsed_data = cell_value

                        # Create a dataframe from the list of dictionaries
                        df_stewards = pd.DataFrame(parsed_data)

                        df_users, schema_file = self.get_valueset_for_tables_sql_xlsx(
                            "User")

                        # Perform left join on 'oid' (from df_stewards) and 'user_id' (from df_users)
                        merged_df = df_stewards.merge(
                            df_users, left_on='oid', right_on='user_id', how='left')

                        # Drop the redundant 'oid' column from df_users
                        merged_df.drop(columns='user_id', inplace=True)

                        # Create the comma-delimited list in the desired format
                        user_list = [f"{row['user_full_name']} ({row['user_email']}:{row['oid']})"
                                     for _, row in merged_df.iterrows()]

                        # Join the list elements with commas
                        comma_delimited_list = ", ".join(user_list)

                        # Replace the cell value with the parsed HTML
                        # This assumes that you want the first table, as pd.read_html returns a list of tables
                        df_tables.loc[idx, column] = comma_delimited_list

                    except Exception as ex:
                        error_msg = f"Error: {str(ex)}"
                        exc_info = sys.exc_info()
                        logger_singleton.error_with_exception(
                            error_msg, exc_info)
                        pass

            # Get valid html columns from expected table structure
            valid_html_columns = self.get_valid_html_columns_from_schema_xlsx(
                df_fields_excel_schema, df_tables)

            # Convert valid html columns
            for column in valid_html_columns:
                # for each row in the column
                for idx in df_tables.index:
                    # Get the value at the current cell
                    cell_value = df_tables.loc[idx, column]
                    try:
                        # Try to parse it as HTML
                        if cell_value is None:
                            cell_value = ''

                        if pd.isna(cell_value):
                            cell_value = ''

                        soup = BeautifulSoup(cell_value, 'html.parser')

                        # Check if 'html' and 'body' tags exist
                        if not soup.html:
                            soup = BeautifulSoup(
                                '<html><body>' + str(soup) + '</body></html>', 'html.parser')

                        # Extract text from the HTML document
                        text = soup.get_text()

                        # Replace the cell value with the parsed HTML
                        # This assumes that you want the first table, as pd.read_html returns a list of tables
                        df_tables.loc[idx, column] = text
                    except ValueError:
                        # pd.read_html throws a ValueError if it can't parse the input as HTML
                        # If this happens, we'll just leave the cell value as it is
                        pass

            # Get ordered columns
            df_ordered_columns = df_fields_excel_schema[
                df_fields_excel_schema['excel_column_order'] > 0]

            # Create a list of column names from df_fields_excel_schema in the order specified by excel_column_order
            ordered_columns = df_ordered_columns.sort_values('excel_column_order')[
                'field_name'].tolist()

            # Get a list of columns that exist in both df_tables and ordered_columns
            table_column_names = df_tables.columns.tolist()
            valid_columns = [
                col for col in ordered_columns if col in table_column_names]

            # Get the intersection of valid_columns and df_tables.columns to preserve valid column order
            valid_columns_present = [
                col for col in valid_columns if col in df_tables.columns]

            # Get the list of columns not in valid_columns and append them at the end
            other_columns = [
                col for col in df_tables.columns if col not in valid_columns]

            # Reorder the DataFrame columns using the desired order
            df_tables = df_tables[valid_columns_present + other_columns]

            # Create a list of columns to hide from df_tables
            columns_to_hide = [
                col for col in df_tables.columns.tolist() if col not in valid_columns]

            # Drop the columns from df_tables
            # df_tables = df_tables.drop(columns=columns_to_drop)

            # Set the option to display all columns
            pd.set_option('display.max_columns', None)
            df_tables = df_tables.fillna('')

            print(df_tables)

            return df_tables, columns_to_hide, df_fields_excel_schema

    def get_table_extra_description_fields(self, table_json):
        """
            Retrieves extra description fields from the table JSON.

            Args:
                table_json (dict): The JSON data representing the table.

            Returns:
                dict: A dictionary containing the extra description fields.

            Raises:
                Exception: If an error occurs while retrieving the extra description fields.

        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_table_extra_description_fields"):

            try:

                extra_description_fields = {}
                if "extraDescriptionFields" in table_json:
                    optional_description_fields = table_json['extraDescriptionFields']
                    msg = "Extra description fields: %s", optional_description_fields
                    logger.info(msg)
                    for key in optional_description_fields:
                        extra_description_fields[key] = optional_description_fields[key]
                return extra_description_fields
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def format_description(self, table_json):
        """
        Formats the description for the table.

        Args:
            table_json (dict): The JSON data representing the table.

        Returns:
            str: The formatted description string.

        Raises:
            Exception: If an error occurs while formatting the description.

        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("format_description"):

            try:

                description = table_json.get('description')
                if self.extra_description_fields:
                    description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
                    for key in self.extra_description_fields:
                        description += '<tr><td>' + key + '</td><td>' + \
                            self.extra_description_fields[key] + '</td></tr>'
                    description += '</table>'
                return description
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
