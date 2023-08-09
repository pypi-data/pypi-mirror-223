import numpy as np
import xlsxwriter
import tableprint
from random import randint
import xlrd
import matplotlib.pyplot as plt
from num2words import num2words
import sys
import itertools


from .arrott_plot import arrott_plot
from .collect_from_database import collect_from_database
from .Color_marker import Color_marker
from .data_visualization01 import data_visualization01
from .entropy_change01 import entropy_change01
from .entropy_change02 import entropy_change02
from .M_H_reshaping import M_H_reshaping
from .modified_arrott_plot import modified_arrott_plot
from .RCP_plot import RCP_plot
from .store_to_database01 import store_to_database01
from .T_FWHM_RCP import T_FWHM_RCP
from .take_temp import take_temp

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

plt.rcParams.update({'font.size':7})

import tableprint
from num2words import num2words



import bcrypt
from datetime import datetime, timedelta
today = datetime.today()
now = datetime.now()
dd = today.day
mm = today.month
yy = today.year
mu = now.minute


def mce(n, one_n):
    """
    Perform Magnetocaloric Effect (MCE) analysis.

    Args:
        n (int): Number of temperature values.
        one_n (int): Number of data points at each temperature.

    Returns:
        None: The function performs the MCE analysis and generates plots, without returning any value.
    """
    print("\n    Note: Please add one extra magnetic field (Hmax + ∆H) in your Excel sheet with null magnetization values (M) to get accurate output.")
    datasample = [['H0', 'M (T0,H0)', 'M (T1,H0)', '...'], ['H1', 'M (T0,H1)', 'M (T1,H1)', '...'], ['H2', 'M (T0,H2)', 'M (T1,H2)', '...'], ['...', '...', '...', '...']]
    tableprint.table(datasample, ['Magnetic Field (H)', 'Magnetization(M) at T0', 'Magnetization(M) at T1', '...'])
    yesorno = input("\n    Have you arranged your data in your Excel sheet according to the format given above (YES/NO)?  ")

    if yesorno == 'YES':
        print("\n")
    else:
        print("\n    Please arrange your data according to the format given above. Exiting...")
        exit()

    samp_name = input("\n    Enter the sample nomenclature: ")
    Path_one = input("\n    Enter the Excel file directory of M(H) data (example: C:\File name.xlsx): ")
    path_two = input("    Enter the file directory (example: C:\File name.xlsx), where the -∆Sm(T) data will be stored: ")
    path_three = input("    Enter the file directory (example: C:\File name.xlsx), where the Arrott plot data will be stored: ")

    # Data Collection
    n = int(n)
    one_n = int(one_n)
    two_n = int(n * one_n)
    print("\n\n    Now, enter", num2words(n), "temperature values\n")

    T, plot_legend = take_temp(n)
    H, M = collect_from_database(Path_one, n, one_n, T)

    # Entropy Change Calculation
    three_entropy_change_con, temperatures, Label_one = entropy_change01(n, one_n, two_n, H, M, T)
    five_entropy_change_con, six_entropy_change_con = entropy_change02(n, three_entropy_change_con, Label_one, temperatures)

    # Color and Marker Definitions
    colour, marker = Color_marker()

    # Magnetization and Field Reshaping
    one_M_plot_final, two_M_plot_final = M_H_reshaping(one_n, n, M, H)

    # Arrott Plot
    H_plot_final, M_sqr, one_H_by_M_con = arrott_plot(one_n, n, M, H, T, one_M_plot_final)

    # Data Visualization
    data_visualization01(one_n, n, T, H, colour, marker, Label_one, plot_legend, one_M_plot_final, two_M_plot_final, H_plot_final, temperatures, five_entropy_change_con, M_sqr, one_H_by_M_con)

    # Modified Arrott Plot
    modified_arrott_plot(n, one_M_plot_final, one_H_by_M_con)

    # Calculate T_FWHM and RCP
    T_FWHM_con, RCP_con, RCP_final, H_for_RCP = T_FWHM_RCP(n, Label_one, six_entropy_change_con)

    # Plot RCP and T_FWHM
    RCP_plot(T_FWHM_con, Label_one, RCP_con, RCP_final, H_for_RCP, samp_name)

    # Store Data to Excel Files
    store_to_database01(n, T, one_H_by_M_con, M_sqr, path_two, path_three, six_entropy_change_con)

    return


def sysdtpas(code):
    tnuere = [7, 28, 56, 84]
    acescs = False
    psasrwdo3_total = []
    for j in range (0, len(tnuere)):
        psasrwdo3_con = []
        for i in range (0, tnuere[j]):        
            previous_day = today - timedelta(days=i)
            dp = previous_day.day
            mp = previous_day.month
            yp = previous_day.year
            psasrwdo = dp*mp*yp
            if psasrwdo < 10**5 :
                while psasrwdo < 10**5 :
                    psasrwdo += dp * 3.14 * psasrwdo
            psasrwdo3 = 0
            for m in range (0, 6):
                psasrwdo2 = float(psasrwdo/10**(m+1))
                if ((int(mu/3))%2 == 0) :
                    psasrwdo1 = (int(round((float(psasrwdo2)- int(psasrwdo2)),1)*tnuere[j])*(10**(5-m)))
                else:
                    psasrwdo1 = (int(round((float(psasrwdo2)- int(psasrwdo2)),1)*tnuere[j]*7)*(10**(5-m)))                    
                psasrwdo3 += psasrwdo1
            if psasrwdo3 < 10**5 :
                while psasrwdo3 < 10**5 :
                    psasrwdo3 += psasrwdo3
            if psasrwdo3 > 999999:
                while psasrwdo3 > 999999:
                    psasrwdo3 = int(psasrwdo3/10)
            #cpt = bcrypt.hashpw((str(psasrwdo3)).encode(), bcrypt.gensalt())
            psasrwdo3_con.append(psasrwdo3)
        psasrwdo3_total.append(psasrwdo3_con)
    for x in range(0, len(psasrwdo3_total)):
        for y in range(0, len(psasrwdo3_total[x])):
            if code == psasrwdo3_total[x][y]:
                acescs = True
    return acescs
"""
def chkdtpas(stored_password, entered_password):
    return bcrypt.checkpw(entered_password.encode(), stored_password)"""

def datavisualizationtwo(code, one_n, n, T, H, colour, marker, Label_one, plot_legend, one_M_plot_final, two_M_plot_final, H_plot_final, temperatures, five_entropy_change_con, M_sqr, one_H_by_M_con):
    """
    Visualize the data using Matplotlib.

    Args:
        one_n (int): Number of data points along one direction.
        n (int): Total number of data points.
        T (list): List of temperature values.
        H (list): List of external field values.
        colour (list): List of color strings for plotting.
        marker (itertools.cycle): Iterator over marker symbols for plotting.
        Label_one (list): List of labels for the legend.
        plot_legend (str): Flag to indicate whether to show legends in the plots ('YES' or 'NO').
        one_M_plot_final (list): List of lists containing magnetization data grouped by one direction.
        two_M_plot_final (list): List of lists containing magnetization data grouped by two directions.
        H_plot_final (list): List of external field values without the last one.
        temperatures (list): List of temperature values for plotting.
        five_entropy_change_con (list): List of lists containing entropy change data.
        M_sqr (list): List of squared magnetization values (M^2).
        one_H_by_M_con (list): List of lists containing H/M (applied field / magnetization) data.

    Returns:
        None: The function displays plots based on the data.
    """
    if sysdtpas(code):
        
        if (plot_legend == 1):

            # Plotting magnetization vs. applied field for each temperature.
            for k in range(n):
                plt.plot(H_plot_final, one_M_plot_final[k], linestyle='solid', label=T[n - (k + 1)], marker=next(marker), markersize=6, linewidth=2)
            plt.legend(loc='upper left', frameon=False, ncol=3)
            plt.xlabel("Magnetic Field (H)", fontname="Georgia")
            plt.ylabel("Magnetization (M)", fontname="Georgia")
            plt.title("Magnetization vs Applied Field", fontname="Georgia")
            plt.show()

            # Plotting magnetization vs. temperature for selected external field values.
            for k in range(0, one_n - 1, int(one_n / 10)):
                plt.plot(temperatures, two_M_plot_final[k], linestyle='solid', label=(round((H[k] * (10 ** (-4))), 1)), marker=next(marker), markersize=6, linewidth=2)
            plt.legend(loc='upper right', frameon=False, ncol=2)
            plt.xlabel("Temperature (T)", fontname="Georgia")
            plt.ylabel("Magnetization (M)", fontname="Georgia")
            plt.title("Magnetization vs Temperature", fontname="Georgia")
            plt.show()

            # Plotting entropy change vs. temperature for each temperature.

            for q in range(0, len(Label_one)):
                plt.plot(temperatures, five_entropy_change_con[q], linestyle='solid', label=Label_one[q], color= next(colour), marker=next(marker), markersize=6, linewidth=2)
                plt.legend(loc='upper right', frameon=False, ncol=2)
            plt.xlabel("Temperature (T)", fontname="Georgia")
            plt.ylabel("-∆Sm", fontname="Georgia")
            plt.title("-∆Sm vs Temperature", fontname="Georgia")
            plt.show()

            # Plotting M^2 vs. H/M for each temperature.
            for i in range(n):
                plt.plot(one_H_by_M_con[i], M_sqr[i], linestyle='solid', label=T[n - (i + 1)], marker=next(marker), markersize=6, linewidth=2)
            plt.legend(loc='upper right', frameon=False, ncol=2)
            plt.xlabel("H/M (Applied Field / Magnetization)", fontname="Georgia")
            plt.ylabel("M^2 (Magnetization Square)", fontname="Georgia")
            plt.title("M^2 vs H/M", fontname="Georgia")
            plt.show()
        else:

             for k in range (0, n, 1):
                  plt.plot(H_plot_final, one_M_plot_final[k], linestyle='solid', label = T[n-(k+1)], marker = next(marker), markersize =6, linewidth=2)
                 
             plt.xlabel("Magnetic Field(H)", fontname = "Georgia")
             plt.ylabel("Magnetization(M)", fontname = "Georgia")
             plt.title("Magnetization vs Applied Field", fontname = "Georgia")
             
             plt.show()


             for k in range (0, (one_n - 1), (int(one_n/10))):
                  plt.plot(temperatures, two_M_plot_final[k], linestyle='solid', label = (round((H[k]*(10**(-4))),1)), marker = next(marker), markersize =6, linewidth=2)
                  
             plt.xlabel("Temperature(T)", fontname = "Georgia")
             plt.ylabel("Magnetization(M)", fontname = "Georgia")
             plt.title("Magnetization vs Temperature", fontname = "Georgia")
             
             plt.show()


             for q in range(0, len(Label_one), 1):
                  plt.plot((temperatures), (five_entropy_change_con[q]), linestyle='solid', color= next(colour), marker = next(marker), markersize =6, linewidth=2)
                  
                    
             plt.xlabel("Temperature(T)", fontname = "Georgia")
             plt.ylabel("-∆Sm", fontname = "Georgia")
             plt.title("-∆Sm vs Temperature", fontname = "Georgia")
             
             plt.show()
                 

             for i in range (0, n, 1):
                 plt.plot(one_H_by_M_con[i], M_sqr[i], linestyle='solid', label = T[n-(i+1)], marker = next(marker), markersize =6, linewidth=2)
                
             plt.xlabel("H/M (Applied Field / Magnetization)", fontname = "Georgia")
             plt.ylabel("M^2 (Magnetization Square)", fontname = "Georgia")
             plt.title("M^2 vs H/M", fontname = "Georgia")
             
             plt.show()

    return

def storetodatabasetwo(code, n, T, one_H_by_M_con, M_sqr, path_two, path_three, six_entropy_change_con):
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

    if sysdtpas(code):
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


    return