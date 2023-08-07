import datetime
from typing import Type

import numpy as np
import pandas as pd


class DataFrameChecker:
    """
    Class for ensuring the validity and consistency of a pandas DataFrame, primarily tailored for
    vibration data. It offers various methods to check and transform the DataFrame to meet specific criteria.

    Attributes:
        dataframe (pd.DataFrame): Input DataFrame to be checked and transformed.

    Methods:
        check_empty_dataframe: Asserts if the DataFrame is non-empty.
        fill_na_and_drop: Fills null values with zeros and optionally drops the 'time' column.
        check_expected_columns: Ensures the presence of specific columns in the DataFrame.
        check_positive_values: Validates that all values in the DataFrame are non-negative.
        check_datatype_float: Confirms that all columns are of float datatype.
        get_dataframe: Returns the processed DataFrame.
        pipeline_checker: A convenience method that applies a sequence of checks and transformations.
        _log_failure: Logs exceptions to a specified file.
    """

    def __init__(self, dataframe) -> None:
        """
        Initializes the DataFrameChecker with a pandas DataFrame.

        Args:
            dataframe (pd.DataFrame): The input pandas DataFrame to be checked and transformed.
        """
        self.dataframe = dataframe

    def check_empty_dataframe(self) -> 'DataFrameChecker':
        """
        Check if the DataFrame is empty.

        Raises:
            ValueError: If the DataFrame is empty.

        Returns:
            DataFrameChecker: Returns self to allow method chaining.
        """
        if self.dataframe.empty:
            raise ValueError('The DataFrame is empty!')
            _log_failure(e)
        return self

    def fill_na_and_drop(self) -> 'DataFrameChecker':
        """
        Fill null values with zero.

        Returns:
            DataFrameChecker: Returns self to allow method chaining.
        """
        self.dataframe = self.dataframe.fillna(0)

        if 'time' in self.dataframe.columns:
            self.dataframe.drop(columns=['time'], inplace=True)
        return self

    def check_expected_columns(self) -> 'DataFrameChecker':
        """
        Verify the DataFrame contains the expected columns.

        Raises:
            ValueError: If any expected column is missing.

        Returns:
            DataFrameChecker: Returns self to allow method chaining.
        """
        expected_columns = ['vibration_x', 'vibration_y', 'vibration_z']
        existing_columns = self.dataframe.columns
        for col in expected_columns:
            if col not in existing_columns:
                raise ValueError(f"Expected column '{col}' not found!")
        return self

    def check_positive_values(self) -> 'DataFrameChecker':
        """
        Check if all columns have only positive values.

        Raises:
            ValueError: If any column contains negative values.

        Returns:
            DataFrameChecker: Returns self to allow method chaining.
        """
        if (self.dataframe < 0).any().any():
            raise ValueError('The DataFrame contains negative values!')
            _log_failure(e)
        return self

    def check_datatype_float(self) -> 'DataFrameChecker':
        """
        Validate the datatype of all columns to ensure they are float.

        Raises:
            ValueError: If any column doesn't have a float datatype.

        Returns:
            DataFrameChecker: Returns self to allow method chaining.
        """
        for column in self.dataframe.columns:
            if self.dataframe[column].dtype != np.float64:
                raise ValueError(
                    f'Column {column} does not have float datatype!'
                )
                _log_failure(e)
        return self

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the processed pandas DataFrame.

        Returns:
            pd.DataFrame: The validated and transformed pandas DataFrame.
        """
        return self.dataframe

    def pipeline_checker(self) -> pd.DataFrame:
        """
        Execute a series of checks and transformations on the DataFrame.

        Returns:
            pd.DataFrame: The validated and transformed pandas DataFrame.
        """

        self.check_empty_dataframe()
        self.fill_na_and_drop()
        self.check_expected_columns()
        self.check_positive_values()
        self.check_datatype_float()

        return self.get_dataframe()

    def _log_failure(e):
        """
        Log the exception to a failure log file.

        This function writes details of the provided exception 'e' to a
        file named 'failure.log' located in the 'logs' directory. If the file
        or directory does not exist, it will be created.

        Parameters:
        - e (Exception): The exception instance to be logged.

        Returns:
        None

        Example:
        >>> try:
        ...     1/0
        ... except Exception as ex:
        ...     _log_failure(ex)
        """

        LOG_DUMP_PATH = 'logs/failure.log'

        with open(LOG_DUMP_PATH, 'a') as fLog:
            fLog.write(f'{datetime.datetime.now()} - Failure: {str(e)}\n')
