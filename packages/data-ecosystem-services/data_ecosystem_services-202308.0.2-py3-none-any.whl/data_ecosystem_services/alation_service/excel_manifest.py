import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import xlsxwriter
import xlsxwriter.utility
from datetime import datetime, timedelta, date

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging
)

from data_ecosystem_services.alation_service import (
    db_table as alation_table
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as cdc_env_file
)

from .token import TokenEndpoint

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
TIMEOUT_ONE_MIN = 60  # or set to whatever value you want
ENVIRONMENT = "dev"


# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the project root directory by going up one or more levels
project_root = os.path.dirname(os.path.dirname(current_script_path))

# Change the current working directory to the project root directory
os.chdir(project_root)
REPOSITORY_PATH_DEFAULT = str(Path(os.getcwd()))


class ManifestExcel:
    """
    This class encapsulates the functionalities to generate Excel file data for a given Alation schema ID and 
    configuration, and to create an Excel file using the data generated.

    The class includes the following methods:
    - convert_dict_to_csv: A static method that takes a dictionary as input and converts it to a string 
      representation in the CSV format.
    - generate_excel_file_data: A class method that generates data for an Excel file given a Alation schema ID 
      and configuration. It uses data from Alation and builds DataFrames to represent the schema and table data. 
      It returns a tuple containing the DataFrame containing the schema data, the DataFrame containing the 
      table data, and the filename of the generated Excel file.
    - generate_excel_file_from_data: A class method that generates an Excel file using DataFrame objects and 
      saves it.

    This class is typically used in scenarios where data from an Alation schema needs to be exported as an Excel file 
    for further analysis or manipulation. The Excel file created includes two sheets, namely 'Instructions' 
    and 'Tables', which hold the schema and table data respectively.

    Note:
    - The generate_excel_file_data method assumes the existence of an `alation_schema` module with a `Schema` class.
    - This method relies on external logging and tracing modules (`logger_singleton` and `tracer_singleton`) that 
      are not provided here.
    - The configuration dictionary (`config`) is expected to contain specific keys such as 'repository_path', 
      'environment', 'edc_alation_user_id', 'edc_alation_base_url', etc.
    - The methods make use of the `pd.DataFrame` function from the `pandas` library to create DataFrames.
    - The generate_excel_file_from_data method uses the xlsxwriter library to create and manipulate the Excel file.
    - The get_column_letter function is assumed to be imported from the openpyxl.utils module.
    """

    @staticmethod
    def convert_dict_to_csv(dictionary):

        return 'UNSUPPORTED LIST'

        if isinstance(dictionary, dict):
            csv_rows = []
            for key, value in dictionary.items():
                csv_row = f"{key}:{value}"
                csv_rows.append(csv_row)
            csv_data = ','.join(csv_rows)
            return csv_data
        else:
            return None

    @classmethod
    def generate_excel_file_data(cls, alation_schema_id, config, json_schema_file_path):
        """
        Generate Excel file data for the given Alation schema ID and configuration.

        Args:
            alation_schema_id (int): The ID of the Alation schema.
            config (dict): A dictionary containing the configuration settings.

        Returns:
            tuple: A tuple containing the following elements:
                - df_schema (pandas.DataFrame): The DataFrame containing the schema data.
                - df_table_list (pandas.DataFrame): The DataFrame containing the table data.
                - manifest_excel_file (str): The file name of the generated Excel file.

        Raises:
            Exception: If there is an error during the generation process.

        This method generates Excel file data for the specified Alation schema ID and configuration settings.
        It retrieves the necessary data from Alation using the provided credentials and builds DataFrames
        to represent the schema and table data.

        The method returns a tuple containing the following elements:
        - df_schema: The DataFrame containing the schema data with columns 'type', 'field_name', and 'value'.
        - df_table_list: The DataFrame containing the table data with columns based on the dictionary keys.
        - manifest_excel_file: The file name of the generated Excel file.

        Note:
        - This method assumes the existence of an `alation_schema` module with a `Schema` class.
        - The method relies on external logging and tracing modules (`logger_singleton` and `tracer_singleton`) that are not provided here.
        - The configuration dictionary (`config`) is expected to contain specific keys such as 'repository_path', 'environment', 'edc_alation_user_id', 'edc_alation_base_url', etc.
        - The method makes use of the `pd.DataFrame` function from the `pandas` library to create DataFrames.
        """

        from data_ecosystem_services.alation_service import (
            db_schema as alation_schema
        )
        schema = alation_schema.Schema()

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        schema_id = alation_schema_id
        schema_name = None
        alation_datasource_id = None
        with tracer.start_as_current_span("generate_excel_file_data"):
            try:

                # Get Parameters
                repository_path = config.get("repository_path")
                environment = config.get("environment")
                alation_user_id = config.get("edc_alation_user_id")
                edc_alation_base_url = config.get("edc_alation_base_url")
                token_endpoint = TokenEndpoint(
                    edc_alation_base_url)
                status_code, edc_alation_api_token, api_refresh_token = token_endpoint.get_api_token_from_config(
                    config)

                print(
                    f"edc_alation_api_token_length: {str(len(edc_alation_api_token))}")
                print(
                    f"api_refresh_token_length: {str(len(api_refresh_token))}")
                assert status_code == 200

                # Get Datasource and Schema Results
                schema_result, datasource_result = schema.get_schema(
                    edc_alation_api_token, edc_alation_base_url, schema_id)

                schema_result_json = schema_result.json()
                alation_datasource_id = schema_result_json[0].get("ds_id")

            except Exception as ex_generic:
                error_msg = str(ex_generic),
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

            # Pandas Dataframes
            try:

                schema_result_json = schema_result.json()
                schema_name = schema_result_json[0].get("name")

                datasource_title = datasource_result.get("title")

                # Create schema result dictionary
                simple_dict = {i: (k, v) for i, (k, v) in enumerate(
                    schema_result.json()[0].items()) if not isinstance(v, list) and not isinstance(v, dict)}
                custom_dict = schema_result.json()[0]['custom_fields']

                # Get Excel File Name using schema name
                manifest_excel_file = schema.get_excel_manifest_file_path(
                    "download", repository_path, datasource_title, schema_name, environment, alation_user_id)

                #  Create schema result data frame
                df_schema_standard = pd.DataFrame.from_dict(simple_dict, orient='index', columns=[
                    'field_name', 'value'])

                # Add column 'type' to the DataFrame for standard fields
                df_schema_standard = df_schema_standard.assign(type='standard')

                # Create custom fields DataFrame
                df_schema_custom = pd.DataFrame(
                    custom_dict)

                # Add column 'type' to the DataFrame for custom fields
                df_schema_custom = df_schema_custom.assign(type='custom')

                # Select columns 'type', 'field_name', and 'value' from each DataFrame
                df_custom_selected = df_schema_custom[[
                    'type', 'field_name', 'value']]
                df_standard_selected = df_schema_standard[[
                    'type', 'field_name', 'value']]

                # Concatenate the two selected DataFrames
                concatenated_df = pd.concat(
                    [df_custom_selected, df_standard_selected])

                # Sort the concatenated DataFrame based on 'type' and 'field_name'
                df_schema = concatenated_df.sort_values(
                    ['type', 'field_name'], ascending=[False, True])

                # Loop through each column and
                for column in df_schema.columns:
                    # convert numeric values to 0
                    if np.issubdtype(df_schema[column].dtype, np.number):
                        df_schema[column].fillna(0, inplace=True)
                    # convert dictionary objects to string
                    if df_schema[column].dtype == 'object':
                        df_schema[column] = df_schema[column].apply(
                            lambda x: cls.convert_dict_to_csv(x) if isinstance(x, dict) else x)
                        df_schema[column] = df_schema[column].astype(
                            str)

                # Initialize table object
                table = alation_table.Table(None, json_schema_file_path)

                # Get table list
                df_table_list, columns_to_hide, df_fields_excel_schema = table.get_tables_for_schema_for_excel(
                    config, alation_datasource_id, alation_schema_id)

                # Return DataFrames
                return df_schema, df_table_list, manifest_excel_file, columns_to_hide, df_fields_excel_schema

            except Exception as ex:
                error_msg = "Error: {str(ex)}",
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def read_manifest_excel_file_tables_worksheet(cls, manifest_excel_file):

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("read_excel_file_data_for_tables"):

            worksheet_name = "Tables"
            # Read the Excel file into a dataframe, starting from cell E7
            # Skip the first 6 rows to start from E7
            df_table_list = pd.read_excel(
                manifest_excel_file, sheet_name=worksheet_name, skiprows=6)

            # Drop the first column
            df_table_list.drop(df_table_list.columns[0], axis=1, inplace=True)

            logger.info(f"df_table_list length: {len(df_table_list.columns)}")

            # Now, 'df_table_list' contains the data from the Excel file starting from cell E7
            return df_table_list

    @classmethod
    def generate_excel_file_from_data(cls, config, columns_to_hide, df_tables_list, manifest_excel_file, df_status, df_steward, df_access_level, df_language, df_update_frequency, df_format, df_fields_excel_schema):
        """
        Generate an Excel file using the given DataFrame objects and save it.

        Args:
            df_schema (pandas.DataFrame): The DataFrame containing schema data.
            df_tables_list (pandas.DataFrame): The DataFrame containing table data.
            manifest_excel_file (str): The file path to save the generated Excel file.

        Returns:
            str: The file path of the generated Excel file.

        Raises:
            None

        This method takes two DataFrame objects, `df_schema` and `df_table_list`, and a file path `manifest_excel_file`.
        It generates an Excel file using the data from the DataFrames and saves it to the specified file path.

        The schema data is written to the "Instructions" sheet, and the table data is written to the "Tables" sheet.
        The columns in both sheets are auto-fitted to accommodate the data.

        The method returns the file path of the generated Excel file once it is saved.

        Note:
        - This method uses the xlsxwriter library to create and manipulate the Excel file.
        - The get_column_letter function is assumed to be imported from the openpyxl.utils module.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("generate_excel_file_from_data"):

            # Create a new xlsxwriter Workbook object
            workbook = xlsxwriter.Workbook(
                manifest_excel_file, {'nan_inf_to_errors': True})

            # Initialize Header Length
            headers = ['Schema attribute', '% Complete',
                       'Last Updated', 'Review By']

            # ws_schema = workbook.add_worksheet('Instructions')

            # # Write df_schema to the "Instructions" sheet
            # for row_num, row in enumerate(df_schema.values.tolist(), start=0):
            #     for col_num, value in enumerate(row):
            #         if isinstance(value, dict):
            #             value = cls.convert_dict_to_csv(value)

            #         ws_schema.write(row_num, col_num, value)

            # Formats

            # Create a format object with bold property
            editable_format = workbook.add_format(
                {'bold': True, 'bg_color': '#4472c4', 'font_color': 'white'})

            # Create a format object with readonly property
            readonly_format = workbook.add_format({
                'bold': True,
                'italic': True,  # Make the text italic
                'bg_color': 'white',
                'font_color': '#7f7f95',
                'border': 1,
                'border_color': 'black'
            })

            # Define the date format for "yyyy-mm-dd".
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            date_format.set_align('left')

            # Create a format with default text setttings for font, size, color and bottom border
            header_text_format = workbook.add_format({
                'font_name': 'Calibri',
                'bold': True,
                'font_size': 15,
                'font_color': '44546A',  # font color
                'bottom': 2,  # enable bottom border
                'bottom_color': '4472C4',  # set bottom border color
            })

            # Worksheets

            ws_table_list = workbook.add_worksheet('Tables')

            # Set the width of the first column to approximately 40 pixels.
            # Excel's column width unit is approximately 1/6 of a character
            ws_table_list.set_column(0, 0, 24 / 6)

            # Write 'Table Updates' in cell G2
            ws_table_list.write('E2', 'Table Updates', header_text_format)

            # Get the headers from the DataFrame and write them to the worksheet first
            headers = df_tables_list.columns.tolist()
            # Initialize list to store max length of each column
            max_length = [len(header) for header in headers]

            header_col_init = 5
            # Apply the bottom border line to the entire row
            for i in range(len(max_length) - (header_col_init - 3)):
                ws_table_list.write(1, i + header_col_init,
                                    ' ', header_text_format)
            environment = config.get('environment')
            obj_file = cdc_env_file.EnvironmentFile()
            app_dir = os.path.dirname(manifest_excel_file)
            parent_dir = os.path.dirname(app_dir)
            schema_path = parent_dir + "/" + environment + "_schema/"
            # Convert 'schema_path' to the current OS directory format
            schema_path = obj_file.convert_to_current_os_dir(schema_path)

            # Join the directory path and the filename using 'os.path.join()'
            json_schema_file = os.path.join(
                schema_path, "manifest.schema.json")
            table = alation_table.Table(None, json_schema_file)

            valid_editable_columns = table.get_valid_editable_fields_from_schema_xlsx(
                df_tables_list)

            valid_required_columns = table.get_valid_required_fields_from_schema_xlsx(
                df_tables_list)

            valid_date_columns = table.get_valid_date_fields_from_schema_xlsx(
                df_fields_excel_schema, df_tables_list)

            # Create valueset reference sheets in the workbook

            # Valueset reference: status_of_dataset
            ws_vs_status = workbook.add_worksheet('status_of_dataset')
            cls.write_dataframe_to_excel(
                workbook, df_status, ws_vs_status, 0, 0, "status_of_dataset")

            # Valueset reference: access_level
            ws_vs_access_level = workbook.add_worksheet('access_level')
            cls.write_dataframe_to_excel(workbook,
                                         df_access_level, ws_vs_access_level, 0, 0, 'access_level')

            # Valueset reference: format
            ws_vs_format = workbook.add_worksheet('format')
            cls.write_dataframe_to_excel(workbook,
                                         df_format, ws_vs_format, 0, 0, 'format')

            # Valueset reference: steward
            ws_vs_steward = workbook.add_worksheet('steward')
            cls.write_dataframe_to_excel(
                workbook, df_steward, ws_vs_steward, 0, 0, 'steward')

            # Valueset reference: language
            ws_vs_language = workbook.add_worksheet('language')
            cls.write_dataframe_to_excel(workbook,
                                         df_language, ws_vs_language, 0, 0, 'language')

            # Valueset reference: update_frequency
            ws_vs_update_frequency = workbook.add_worksheet('update_frequency')
            cls.write_dataframe_to_excel(workbook,
                                         df_update_frequency, ws_vs_update_frequency, 0, 0, 'update_frequency')

            # Table Tab
            # Write Tables on Tables Tab Starting from the C7 cell.
            row_init = 6  # As indexing starts from 0, 7th row corresponds to index 6
            col_init = 1  # As indexing starts from 0, 4th column corresponds to index 1

            ws_table_list.write(
                'E3', 'Instructions: Items in grey are Read-Only.  Update the fields in blue.')
            ws_table_list.write(
                'E4', 'Dropdowns should contain picklist validation.')

            # List to store the column numbers of date columns
            date_col_numbers = []

            # Write headers to the worksheet
            for header_num, header in enumerate(headers):
                # Check if the header is in valid_date_columns
                if header in valid_date_columns:
                    date_col_numbers.append(header_num)

                if header in valid_editable_columns:
                    col_number = header_num + col_init
                    ws_table_list.write(
                        row_init, col_number, header, editable_format)
                else:
                    ws_table_list.write(row_init, header_num +
                                        col_init, header + " (Read-Only)", readonly_format)

            # Get the number of columns in the DataFrame
            num_of_columns = len(df_tables_list.columns)

            # Log the number of columns
            logger.info(
                f"Number of columns in df_tables_list {num_of_columns}")

            # Now iterate over the rows and write them to the worksheet, starting from the second row (index 1)
            for row_num, row in enumerate(df_tables_list.itertuples(index=False), start=1):
                for col_num, value in enumerate(row):
                    # Check if value is a dictionary
                    if isinstance(value, dict):
                        value = cls.convert_dict_to_csv(value)
                    # Check if value is a list
                    elif isinstance(value, list):  # check if value is a list
                        # convert list to string
                        value = ', '.join(map(str, value))

                    if col_num in date_col_numbers:
                        # Convert the date to the desired format
                        ws_table_list.write(row_num + row_init,
                                            col_num + col_init, value, date_format)
                    else:
                        # Write the value to the worksheet
                        ws_table_list.write(row_num + row_init,
                                            col_num + col_init, value)

                    # Update max_length of column width if necessary
                    cell_length = len(str(value))
                    if cell_length > max_length[col_num]:
                        max_length[col_num] = cell_length

            # After writing headers to the worksheet
            # Get the range in the desired format.
            sheet_name_status_of_dataset = "status_of_dataset"
            cell_range_formula_status_of_dataset = cls.get_excel_range(
                df_status, 1, 0, sheet_name_status_of_dataset)

            data_validation_options_status_of_dataset = {
                'validate': 'list',
                'source': cell_range_formula_status_of_dataset
            }

            # Validate status of dataset
            status_of_dataset_col_num = [i for i, header in enumerate(
                headers)
                if header.lower().replace(" ", "_") == "status_of_dataset"]
            if status_of_dataset_col_num:  # If the "status_of_dataset" column is present
                # Adjust column number with col_init
                status_of_dataset_col_num = status_of_dataset_col_num[0] + col_init
                # Apply data validation to the cells in the 'status_of_dataset' column
                ws_table_list.data_validation(
                    f'{xlsxwriter.utility.xl_rowcol_to_cell(row_init + 1, status_of_dataset_col_num)}:{xlsxwriter.utility.xl_rowcol_to_cell(row_init + len(df_tables_list), status_of_dataset_col_num)}', data_validation_options_status_of_dataset)

            # After writing headers to the worksheet
            # Get the range in the desired format.
            sheet_name_access_level = "access_level"
            cell_range_formula_access_level = cls.get_excel_range(
                df_access_level, 1, 0, sheet_name_access_level)

            data_validation_options_access_level = {
                'validate': 'list',
                'source': cell_range_formula_access_level
            }
            # Validate access level
            access_level_col_num = [i for i, header in enumerate(
                headers)
                if header.lower().replace(" ", "_") == "access_level"]
            if access_level_col_num:  # If the "access_level" column is present
                # Adjust column number with col_init
                access_level_col_num = access_level_col_num[0] + col_init
                # Apply data validation to the cells in the 'access_level' column
                ws_table_list.data_validation(
                    f'{xlsxwriter.utility.xl_rowcol_to_cell(row_init + 1, access_level_col_num)}:{xlsxwriter.utility.xl_rowcol_to_cell(row_init + len(df_tables_list), access_level_col_num)}', data_validation_options_access_level)

            # After writing headers to the worksheet
            # Get the range in the desired format.
            sheet_name_format = "format"
            cell_range_formula_format = cls.get_excel_range(
                df_format, 1, 0, sheet_name_format)

            data_validation_options_format = {
                'validate': 'list',
                'source': cell_range_formula_format
            }
            # Validate format
            format_col_num = [i for i, header in enumerate(
                headers)
                if header.lower().replace(" ", "_") == "format"]
            if format_col_num:  # If the "format" column is present
                # Adjust column number with col_init
                format_col_num = format_col_num[0] + col_init
                # Apply data validation to the cells in the 'format' column
                ws_table_list.data_validation(
                    f'{xlsxwriter.utility.xl_rowcol_to_cell(row_init + 1, format_col_num)}:{xlsxwriter.utility.xl_rowcol_to_cell(row_init + len(df_tables_list), format_col_num)}', data_validation_options_format)

            # After writing headers to the worksheet
            # Get the range in the desired language.
            sheet_name_language = "language"
            cell_range_formula_language = cls.get_excel_range(
                df_language, 1, 0, sheet_name_language)

            data_validation_options_language = {
                'validate': 'list',
                'source': cell_range_formula_language
            }
            # Validate language
            language_col_num = [i for i, header in enumerate(
                headers)
                if header.lower().replace(" ", "_") == "language"]
            if language_col_num:  # If the "language" column is present
                # Adjust column number with col_init
                language_col_num = language_col_num[0] + col_init
                # Apply data validation to the cells in the 'language' column
                ws_table_list.data_validation(
                    f'{xlsxwriter.utility.xl_rowcol_to_cell(row_init + 1, language_col_num)}:{xlsxwriter.utility.xl_rowcol_to_cell(row_init + len(df_tables_list), language_col_num)}', data_validation_options_language)

            # Define the date validation rule. In this example, we restrict dates to be within 2022-01-01 and 2022-12-31.
            # Get today's date
            current_date = date.today()

            # Calculate the start_date as 20 years ago from the current date
            start_date = current_date - timedelta(days=365 * 20)

            # Calculate the end_date as one year from the current date
            end_date = current_date + timedelta(days=365)

            # Format the start_date as 'yyyy-mm-dd'
            start_date_formatted = start_date.strftime('%Y-%m-%d')

            # Format the end_date as 'yyyy-mm-dd'
            end_date_formatted = end_date.strftime('%Y-%m-%d')

            data_validation_options_date_standard = {
                'validate': 'date',
                'criteria': 'between',
                'minimum': start_date,
                'maximum': end_date,
                'error_message': 'Enter a date between {} and {}.'.format(start_date_formatted, end_date_formatted),
                'input_message': 'Enter a date between {} and {}.'.format(start_date_formatted, end_date_formatted)
            }

            # List to store the column numbers of all date columns
            date_col_numbers = [i for i, header in enumerate(
                headers) if header in valid_date_columns]

            # Loop through each date column and apply data validation
            for date_col_num in date_col_numbers:
                # Adjust column number with col_init
                date_col_num = date_col_num + col_init
                # Apply data validation to the cells in the 'language' column
                ws_table_list.data_validation(
                    f'{xlsxwriter.utility.xl_rowcol_to_cell(row_init + 1, date_col_num)}:{xlsxwriter.utility.xl_rowcol_to_cell(row_init + len(df_tables_list), date_col_num)}',
                    data_validation_options_date_standard
                )

            # Now set the column widths based on the max length of the data in each column
            for i, width in enumerate(max_length):
                ws_table_list.set_column(i + col_init, i + col_init, width)

            # Hide column B - D
            ws_table_list.set_column('B:D', None, None, {'hidden': True})

            # Hide non required columns
            for header_num, header in enumerate(headers):
                if header not in valid_required_columns:
                    col_number = header_num + col_init
                    cls.hide_column_by_number(ws_table_list, col_number)

            # Hide worksheets
            ws_vs_status.hide()
            ws_vs_access_level.hide()
            ws_vs_format.hide()
            ws_vs_steward.hide()
            ws_vs_language.hide()
            ws_vs_update_frequency.hide()

            # Close the workbook
            workbook.close()

            return manifest_excel_file

    @staticmethod
    def hide_column_by_number(worksheet, column_number):
        """
        Hide a specific column in an XlsxWriter worksheet.

        Parameters:
            worksheet (Worksheet): The XlsxWriter worksheet object where the column should be hidden.
            column_number (int): The zero-based index of the column to be hidden.

        Returns:
            None

        Note:
            This method uses the XlsxWriter's 'set_column()' method to set the width of the specified column to zero,
            effectively hiding it from view. The 'hidden' parameter is set to True in the 'set_column()' method
            to hide the column without deleting its data.

        Example:
            # Create a new Excel workbook and add a worksheet.
            workbook = xlsxwriter.Workbook('hidden_columns.xlsx')
            worksheet = workbook.add_worksheet()

            # Example data - write some data to columns A, B, and C.
            worksheet.write('A1', 'Column A')
            worksheet.write('B1', 'Column B')
            worksheet.write('C1', 'Column C')

            # Hide the second column (column B) by its number (index 1).
            hide_column_by_number(worksheet, 1)

            # Save the workbook.
            workbook.close()
        """
        worksheet.set_column(column_number, column_number,
                             None, None, {'hidden': True})

    @classmethod
    def write_dataframe_to_excel(cls, workbook, df_to_write, worksheet, start_row, start_col, sheet_name):
        """
        Write a pandas DataFrame to an Excel worksheet using XlsxWriter.

        This function creates column headers in the worksheet using the DataFrame's column names 
        and then populates the worksheet with data from the DataFrame. The DataFrame's index is ignored. 
        Each row from the DataFrame is written to a new row in the worksheet, starting from 
        the first row after the headers.

        Args:
            workbook (xlsxwriter.workbook.Workbook): The workbook object where the worksheet resides.
            df_to_write (pandas.DataFrame): The DataFrame to write to the Excel worksheet.
            worksheet (xlsxwriter.worksheet.Worksheet): The worksheet object to write to. This should 
                                                    be a valid Worksheet object created from 
                                                    an XlsxWriter Workbook.
            sheet_name (str, optional): The name of the sheet in the workbook to write to. 
                                        Defaults to 'Sheet1'.

        Returns:
            str: A string "Ok" is returned after successful execution of the function.

        Raises:
            Any exceptions raised during execution will be propagated to the caller.

        Usage:
            ```python
            import xlsxwriter
            import pandas as pd

            workbook = xlsxwriter.Workbook('filename.xlsx')
            worksheet = workbook.add_worksheet('Sheet1')
            df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            write_dataframe_to_excel(workbook, df, worksheet, 'Sheet1')
            workbook.close()
            ```

        Note:
            This function also tries to mix functionality from openpyxl. Ensure you have the right libraries 
            and dependencies installed and that they are compatible with each other.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("write_dataframe_to_excel"):

            # Get the column names from the DataFrame
            columns = df_to_write.columns.tolist()

            # Write the column headers to the worksheet
            for idx, column in enumerate(columns):
                worksheet.write(start_row, idx + start_col, column)

            logger.info(f"Writing DataFrame to Excel worksheet {sheet_name}")
            # Iterate over the DataFrame rows and write each row to the worksheet
            for row_idx, row in df_to_write.iterrows():
                for col_idx, value in enumerate(row):
                    # row_idx+1 because we have headers
                    worksheet.write(row_idx + start_row + 1,
                                    col_idx + start_col, value)

            # Get the range in the desired format.
            cell_range = cls.get_excel_range(
                df_to_write, start_row + 1, start_col, sheet_name)
            logger.info(f"cell_range:{cell_range}")

            named_range_name = f"{sheet_name}_range"

            # Define a named range for the DataFrame range
            workbook.define_name(
                named_range_name, cell_range)

            return "Ok"

    @classmethod
    def get_excel_range(cls, df_to_write: pd.DataFrame, start_row, start_col, sheet_name):
        """
        Creates a fixed Excel cell range from a given DataFrame and starting cell.

        This function creates a copy of the DataFrame and uses the 'start' and 'end' formulas to calculate 
        the starting and ending cell positions in Excel notation. It then forms a range and makes it fixed 
        to prevent the range from shifting.

        Parameters:
        df_to_write (pd.DataFrame): The DataFrame to be written to Excel.
        start_row (int): The starting row index for the DataFrame.
        start_col (int): The starting column index for the DataFrame.
        sheet_name (str): The name of the Excel sheet where the DataFrame will be written.

        Returns:
        cell_range (str): A fixed Excel cell range in the format "=$SheetName!$A$1:$B$2".

        Note:
        This function depends on the 'evaluate_range_formula' method to get the start and end cell references 
        and the 'make_range_fixed' method to create a fixed cell range. Ensure these methods are properly implemented.
        """

        # Create a copy of the DataFrame
        df_copy = df_to_write.copy()

        start_row, start_col = cls.evaluate_range_formula(
            df_copy, "start", start_row, start_col)
        end_row, end_col = cls.evaluate_range_formula(
            df_copy, "end", start_row, start_col)

        start_cell = xlsxwriter.utility.xl_rowcol_to_cell(start_row, start_col)
        end_cell = xlsxwriter.utility.xl_rowcol_to_cell(end_row, end_col)

        cell_range = f"{start_cell}:{end_cell}"

        cell_range_formula = f"={sheet_name}!{cell_range}"

        cell_range = cls.make_range_fixed(cell_range_formula)

        return cell_range

    @staticmethod
    def evaluate_range_formula(df_copy: pd.DataFrame, formula: str, start_row, start_col):
        """
        Evaluates a given formula and returns the row and column numbers based on the formula.

        This function is used to compute the starting and ending cell references within a DataFrame.
        The starting and ending positions are computed based on a provided formula.
        Currently, it supports only two formulas: 'start' and 'end'.

        Parameters:
        df_copy (pd.DataFrame): The DataFrame on which the cell reference formulas will be evaluated.
        formula (str): A string that determines how the function behaves. Currently supports 'start' and 'end'.
        start_row (int): The row number from which to start the evaluation.
        start_col (int): The column number from which to start the evaluation.

        Returns:
        row (int): The evaluated row number based on the given formula.
        col (int): The evaluated column number based on the given formula.

        Note:
        This function is a placeholder. Depending on the complexity and nature of the formulas you are using,
        you may need to implement a more sophisticated version of this function.
        """
        if formula == "start":
            row = start_row
            col = start_col
        if formula == "end":
            row = start_row + (len(df_copy.index) - 1)
            col = start_col + (len(df_copy.columns) - 1)

        return row, col

    @staticmethod
    def make_range_fixed(range_string):
        """
        Converts a regular Excel cell range into a fixed cell range.

        This function takes a cell range in the format "SheetName!A1:B2" and converts it to a fixed cell range 
        in the format "SheetName!$A$1:$B$2". Fixed cell ranges don't shift when copied to other cells in Excel.

        Parameters:
        range_string (str): The Excel cell range to be made fixed. Should be in the format "SheetName!A1:B2".

        Returns:
        fixed_range (str): The fixed Excel cell range. Will be in the format "SheetName!$A$1:$B$2".

        Example:
        >>> make_range_fixed("Sheet1!A1:B2")
        "Sheet1!$A$1:$B$2"
        """
        sheet, range_part = range_string.split("!")
        start, end = range_part.split(":")
        start_col, start_row = ''.join(
            filter(str.isalpha, start)), ''.join(filter(str.isdigit, start))
        end_col, end_row = ''.join(filter(str.isalpha, end)), ''.join(
            filter(str.isdigit, end))
        fixed_range = f"{sheet}!${start_col}${start_row}:${end_col}${end_row}"
        return fixed_range
