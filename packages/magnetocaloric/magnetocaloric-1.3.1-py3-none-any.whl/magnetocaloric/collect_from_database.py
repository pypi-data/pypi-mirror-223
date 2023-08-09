import xlrd

def collect_from_database(Path_one, n, one_n, T):
    """
    Collects magnetization (M) and external fields (H) data from an Excel sheet.

    Parameters:
        Path_one (str): The file path of the Excel sheet.
        n (int): The number of temperature values (columns) in the Excel sheet.
        one_n (int): The number of data rows for each field value (H) in the Excel sheet.
        T (list): A list containing the temperature values.

    Returns:
        H (list): A list containing the external fields data.
        M (list): A list containing the magnetization data.
    """

    # Initialize empty lists to store magnetization (M) and external fields (H) data
    Magnetization_val = []
    External_Fields = []
    M = Magnetization_val
    H = External_Fields

    # Open the Excel file and read the data
    book = xlrd.open_workbook(Path_one)
    sheet = book.sheet_by_name('Sheet1')
    data = [[sheet.cell_value(r, c) for c in range(n + 1)] for r in range(sheet.nrows)]

    # Loop to collect magnetization (M) and external fields (H) data from the Excel sheet
    for a in range(1, one_n + 1, 1):
        H.append((data[a])[0])
        for b in range(0, n):
            T.append(T[b])
        for b in range(1, n + 1):
            M.append((data[a])[b])

    # Return the collected external fields (H) and magnetization (M) data as lists
    return H, M