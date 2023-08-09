import matplotlib.pyplot as plt
import numpy as np

def modified_arrott_plot(n, one_M_plot_final, one_H_by_M_con):
    """
    Generate modified Arrott plots using Matplotlib.

    Args:
        n (int): Number of data points.
        one_M_plot_final (list): List of lists containing magnetization data.
        one_H_by_M_con (list): List of lists containing H/M (applied field / magnetization) data.

    Returns:
        None: The function displays four subplots of modified Arrott plots.
    """
    # Calculate powers of magnetization and H/M for four different β and γ values.
    M_pow_MFT = np.power(one_M_plot_final, 2)
    H_by_M_pow_MFT = np.power(one_H_by_M_con, 1)

    M_pow_TMFT = np.power(one_M_plot_final, 4)
    H_by_M_pow_TMFT = np.power(one_H_by_M_con, 1)

    M_pow_3DH = np.power(one_M_plot_final, (1 / 0.365))
    H_by_M_pow_3DH = np.power(one_H_by_M_con, (1 / 1.336))

    M_pow_3DI = np.power(one_M_plot_final, (1 / 0.325))
    H_by_M_pow_3DI = np.power(one_H_by_M_con, (1 / 1.24))

    # Create four subplots to display the modified Arrott plots.
    plt.subplot(2, 2, 1)
    for i in range(n):
        plt.plot(H_by_M_pow_MFT[i], M_pow_MFT[i], linestyle='solid', linewidth=2)
    plt.xlabel("(H/M)^(1/γ)", fontname="Georgia")
    plt.ylabel("M^(1/β)", fontname="Georgia")
    plt.title("Arrott plot 01 (β:0.5; γ:1)", fontname="Georgia")

    plt.subplot(2, 2, 2)
    for i in range(n):
        plt.plot(H_by_M_pow_TMFT[i], M_pow_TMFT[i], linestyle='solid', linewidth=2)
    plt.xlabel("(H/M)^(1/γ)", fontname="Georgia")
    plt.ylabel("M^(1/β)", fontname="Georgia")
    plt.title("Arrott plot 02 (β:0.25; γ:1)", fontname="Georgia")

    plt.subplot(2, 2, 3)
    for i in range(n):
        plt.plot(H_by_M_pow_3DH[i], M_pow_3DH[i], linestyle='solid', linewidth=2)
    plt.xlabel("(H/M)^(1/γ)", fontname="Georgia")
    plt.ylabel("M^(1/β)", fontname="Georgia")
    plt.title("Arrott plot 03 (β:0.365; γ:1.336)", fontname="Georgia")

    plt.subplot(2, 2, 4)
    for i in range(n):
        plt.plot(H_by_M_pow_3DI[i], M_pow_3DI[i], linestyle='solid', linewidth=2)
    plt.xlabel("(H/M)^(1/γ)", fontname="Georgia")
    plt.ylabel("M^(1/β)", fontname="Georgia")
    plt.title("Arrott plot 04 (β:0.325; γ:1.24)", fontname="Georgia")

    # Adjust the layout and display the subplots.
    plt.tight_layout()
    plt.show()

    return