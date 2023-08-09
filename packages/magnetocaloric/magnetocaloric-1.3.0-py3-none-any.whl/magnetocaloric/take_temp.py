def take_temp(n):
    """
    Collects temperature values from the user and asks for plot_legend choice.

    Parameters:
        n (int): The number of temperature values to collect.

    Returns:
        T (list): A list containing the collected temperature values.
        plot_legend (str): The user's choice for plotting with legend ("YES" or "NO").
    """

    # Initialize an empty list to store temperature values
    Temperature_vals = []
    T = Temperature_vals

    # Loop to collect n temperature values from the user
    for b in range(0, n):
        Temperature_val = input("    enter the temperature value : ")
        T.append(Temperature_val)

    # Prompt the user for plot_legend choice
    plot_legend = input("\n\n    do you want to plot the figures with legend (YES/NO)?  ")

    # Return the list of temperature values and the user's plot_legend choice
    return T, plot_legend
