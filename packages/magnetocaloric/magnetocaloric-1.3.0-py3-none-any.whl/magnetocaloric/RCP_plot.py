import numpy as np
import matplotlib.pyplot as plt

def RCP_plot(T_FWHM_con, Label_one, RCP_con, RCP_final, H_for_RCP, samp_name):
    """
    Plot Relative Cooling Power (RCP) and Full Width at Half Maximum (T_FWHM) against magnetic field (H).

    Args:
        T_FWHM_con (list): List of calculated FWHM values.
        Label_one (list): List of temperature values.
        RCP_con (list): List of calculated RCP values for all temperatures.
        RCP_final (list): List of RCP values with sufficient data.
        H_for_RCP (list): List of magnetic field values corresponding to RCP.
        samp_name (str): Name of the sample.

    Returns:
        None: The function only plots the RCP/T_FWHM vs H graphs.
    """
    samp_name_plus_RCP = "RCP (" + samp_name + ") :: max val : " + str(np.max(RCP_con))
    samp_name_plus_T_FWHM = "T_FWHM (" + samp_name + ") :: max width : " + str(np.max(T_FWHM_con))

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Magnetic Field(H)", fontname="Georgia")
    ax1.set_ylabel("RCP", fontname="Georgia")
    ax1.plot(Label_one, RCP_con, linestyle='solid', marker='h', label=samp_name_plus_RCP, color='b', markersize=6, linewidth=2)
    ax1.legend(loc='upper left', frameon=False, ncol=2)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel("T_FWHM", fontname="Georgia")
    ax2.plot(Label_one, T_FWHM_con, linestyle='none', marker='H', label=samp_name_plus_T_FWHM, color='c', markersize=2, linewidth=0.5)
    ax2.legend(loc='lower right', frameon=False, ncol=2)
    ax2.tick_params(axis='y')

    plt.title("RCP/T_FWHM vs H", fontname="Georgia")

    plt.show()

    # Plot RCP vs H for cases with sufficient data.
    if len(RCP_final) >= 2:
        plt.xlabel("Magnetic Field(H)", fontname="Georgia")
        plt.ylabel("RCP", fontname="Georgia")
        plt.title("Magnetic Field vs RCP", fontname="Georgia")
        plt.plot(H_for_RCP, RCP_final, linestyle='solid', color='b', marker='h', markersize=6, linewidth=2)
        plt.show()

    return