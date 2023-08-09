import matplotlib.pyplot as plt
import itertools

def data_visualization01(one_n, n, T, H, colour, marker, Label_one, plot_legend, one_M_plot_final, two_M_plot_final, H_plot_final, temperatures, five_entropy_change_con, M_sqr, one_H_by_M_con):
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
    if plot_legend == 'YES':

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