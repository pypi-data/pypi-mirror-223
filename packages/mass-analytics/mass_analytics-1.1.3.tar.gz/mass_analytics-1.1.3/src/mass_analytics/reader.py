import pandas as pd


def read_data(path):
    """ 
    Description:    
        Load data from a CSV or Excel file and return it as a pandas DataFrame.

    Parameters:
        path (str): The path to the CSV or Excel file containing the data.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the CSV or Excel file.

    Raises:
        ValueError: If the file extension is not supported (only .csv and .xlsx/.xls are allowed).
        FileNotFoundError: If the file specified by the path does not exist.
        Exception: For any other unexpected errors during data loading.

    Example:
        >>> data_frame = read_data('data.csv')
        >>> data_frame.head()
              Column1  Column2
        0       1        10
        1       2        15
        2       3        20
        3       4        25
        4       5        30
    """
        
    # Extract file extension
    file_extension = path.split('.')[-1].lower()

    # Check if the file extension is valid
    if file_extension not in ['csv', 'xlsx', 'xls']:
        raise ValueError("Invalid file extension. Only .csv and .xlsx/.xls files are allowed.")

    try:
        # Load data from CSV or Excel file
        if file_extension == 'csv':
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
            
        return df
    except FileNotFoundError:
        raise FileNotFoundError("The file specified by the path does not exist.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading the data: {e}")
        

