import numpy as np

def entropy_change02(n, three_entropy_change_con, Label_one, temperatures):
    """
    Calculate the entropy changes based on the provided data.

    Parameters:
        n (int): Number of temperature values.
        three_entropy_change_con (list): List of lists containing entropy change data.
        Label_one (list): List of magnetic field values in Tesla.
        temperatures (list): List of temperature values.

    Returns:
        five_entropy_change_con (list): List of lists containing entropy change data in (10^-4 J/mol K) units.
        six_entropy_change_con (list): List of lists containing entropy change data along with temperature values.
    """
    six_entropy_change_con = []
    six_entropy_change_con.append(temperatures)
    five_entropy_change_con = []

    for j in range(0, len(Label_one), 1):
        four_entropy_change_con = []

        for i in range(0, n - 1, 1):
            four_entropy_change_con.append((10 ** (-4)) * (three_entropy_change_con[i])[j])

        five_entropy_change_con.append(four_entropy_change_con)
        six_entropy_change_con.append(four_entropy_change_con)

    return five_entropy_change_con, six_entropy_change_con
