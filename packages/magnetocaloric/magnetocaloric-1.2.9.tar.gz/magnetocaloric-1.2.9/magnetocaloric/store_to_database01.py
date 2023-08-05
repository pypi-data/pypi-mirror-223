import xlsxwriter

def store_to_database01(n, T, one_H_by_M_con, M_sqr, path_two, path_three, six_entropy_change_con):
    """
    Store data to two separate Excel spreadsheets.

    Args:
        n (int): Number of data points.
        T (list): List of temperature values.
        one_H_by_M_con (list): List of lists containing H/M values for each temperature.
        M_sqr (list): List of lists containing M^2 values for each temperature.
        path_two (str): Filepath for the first Excel spreadsheet.
        path_three (str): Filepath for the second Excel spreadsheet.
        six_entropy_change_con (list): List of lists containing entropy change values for each temperature.

    Note:
        The function will insert appropriate headers and blank spaces in the data before saving to Excel.
    """
    # Save entropy change data to the first Excel spreadsheet (path_two).
    workbook = xlsxwriter.Workbook(path_two)
    worksheet = workbook.add_worksheet()
    row = 0
    for col, data in enumerate(six_entropy_change_con):
        worksheet.write_column(row, col, data)
    workbook.close()

    # Prepare M^2 vs. H/M data before saving to the second Excel spreadsheet (path_three).
    for i in range(0, 2 * n, 1):
        lo = 2 * i + 1
        T.insert(lo, '   ')

    M_sqr_vs_H_by_M = one_H_by_M_con
    M_sqr_tolist = M_sqr.tolist()

    for i in range(0, n, 1):
        x_index = 2 * i + 1
        M_sqr_vs_H_by_M.insert(x_index, M_sqr_tolist[i])

    for i in range(0, 2 * n, 1):
        M_sqr_vs_H_by_M[i].insert(0, T[i])
        M_sqr_vs_H_by_M[i].insert(1, ' ')
        if i % 2 == 0:
            M_sqr_vs_H_by_M[i].insert(2, 'H/M')
        else:
            M_sqr_vs_H_by_M[i].insert(2, 'M^2')

    # Save M^2 vs. H/M data to the second Excel spreadsheet (path_three).
    workbook = xlsxwriter.Workbook(path_three)
    worksheet = workbook.add_worksheet()
    row = 0
    for col, data in enumerate(M_sqr_vs_H_by_M):
        worksheet.write_column(row, col, data)
    workbook.close()

    print("\n    Check the Excel spreadsheets, data has been successfully saved.")

    return