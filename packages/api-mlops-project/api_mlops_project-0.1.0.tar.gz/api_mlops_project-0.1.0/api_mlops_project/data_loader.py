from typing import Optional, Type

import pandas as pd


class DataLoader:
    """
    Utility class for loading datasets into pandas DataFrames.

    The DataLoader class provides methods for reading data from various file formats
    like CSV, Excel, JSON, and Parquet into pandas DataFrames. It includes mechanisms
    to detect the delimiter used in CSV-like files and also to automatically determine
    the file format if not explicitly provided.

    The primary function is `read_data_dataframe` which, given a file path, will attempt
    to read the file into a DataFrame, detecting or using a specified format.

    Usage:
        data_df = DataLoader.read_data_dataframe('path_to_file.csv')
    """

    @staticmethod
    def detect_sep(data_path: str) -> str:
        """
        Detect the delimiter used in a file, specifically targeting CSV-like files.

        The function checks for common delimiters such as semicolon (;) and comma (,).
        It reads the first line of the file and identifies the delimiter based on its presence.

        Args:
            data_path (str): Path to the file for which the delimiter needs to be detected.

        Raises:
            ValueError: Raises an exception if the delimiter could not be detected, suggesting
            that the file might be in an unsupported format.

        Returns:
            str: The detected delimiter - either a semicolon (;) or a comma (,).
        """
        with open(data_path, 'r') as file:
            first_line = file.readline()

        if ';' in first_line:
            return ';'
        elif ',' in first_line:
            return ','
        else:
            raise ValueError(
                'Delimiter not detected. The file may be in an unsupported format.'
            )

    @staticmethod
    def read_data_dataframe(
        data_path: str, format: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Read data from the given path into a pandas DataFrame based on the specified format.

        This function aims to detect and read various file formats into a pandas DataFrame.
        If the format is not explicitly provided, it infers the format from the file extension.

        Args:
            data_path (str): The path to the data file to be read.
            format (str, optional): The format of the data file (e.g., 'csv', 'xlsx', 'json', 'parquet').
                                    If not provided, it's inferred from the file extension. Defaults to None.

        Raises:
            ValueError: If the format is not supported or unrecognized.

        Returns:
            dataframe (pd.DataFrame): The data read from the file as a pandas DataFrame.
        """
        if format is None:
            format = data_path.split('.')[-1]
        if format in ('csv', 'txt'):
            sep = DataLoader.detect_sep(data_path)
            return pd.read_csv(data_path, sep=sep)
        elif format in ('xls', 'xlsx'):
            return pd.read_excel(data_path)
        elif format == 'json':
            return pd.read_json(data_path)
        elif format == 'parquet':
            return pd.read_parquet(data_path, engine='pyarrow')

        raise ValueError(f"format '{format}' is not supported.")
