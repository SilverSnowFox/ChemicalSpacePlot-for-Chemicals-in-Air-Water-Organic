# Import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

csv_path = input("Enter the file name as example.csv (See sample.csv for example input): ")

try: 
    with open(file=csv_path) as f:
        reader = [row for row in csv.reader(f, delimiter="|")] # Converting the csv reader to a list of lists to then convert to dictionary.
        data = {
            'Compound': reader[0],
            'log(Koa)': [float(i) for i in reader[1]],
            'log(Kaw)': [float(i) for i in reader[2]],
            'log(Koc) (L/kg)': [float(i) for i in reader[3]]
        }

    df = pd.DataFrame(data) 

    # The volumes as input
    Va = float(input("Enter volume of air compartment (m^3): ", ))
    Vom = float(input("Enter volume of soil (or organic) compartment (m^3): ", ))
    Vw = float(input("Enter volume of water compartment (m^3): ", ))


    # Calculating shaded areas
    # Logarithmic ranges for KAW and KOM
    log_kaw_range = np.linspace(-20, 20, 100)
    log_koa_range = np.linspace(-20, 20, 100)
    log_KAW, log_KOA = np.meshgrid(log_kaw_range, log_koa_range)

    # Calculate actual KAW and KOM values from the logarithms
    KAW = 10**log_KAW
    KOA = 10**log_KOA

    Phi_water = 1 / (1 + KAW * (Va / Vw) + (KOA * KAW) * (Vom / Vw))
    Phi_air = 1 / (1 + (1 / KAW) * (Vw / Va) + (KOA) * (Vom / Va))
    Phi_soil = 1 / (1 + (1 / (KOA * KAW)) * (Vw / Vom) + (1 / KOA) * (Va / Vom))


    # Create the CSP plot with color representing log(Kaw)
    plt.figure(figsize=(10, 6))

    plt.contourf(log_KOA, log_KAW, Phi_water, levels=[0.5, 1], colors=['#4752e6'], alpha=0.7)  # Shade the area where Phi_water > threshold
    plt.contour(log_KOA, log_KAW, Phi_water, levels=[0.1, 0.5], colors='black', alpha=0.5)  # Phi_water contours

    plt.contourf(log_KOA, log_KAW, Phi_air, levels=[0.5, 1], colors=['#4e9159'], alpha=0.7)  # Shade the area where Phi_air > threshold
    plt.contour(log_KOA, log_KAW, Phi_air, levels=[0.1, 0.5], colors='black', alpha=0.5)  # Phi_water contours

    plt.contourf(log_KOA, log_KAW, Phi_soil, levels=[0.5, 1], colors=['#d44444'], alpha=0.5)  # Shade the area where Phi_soil > threshold
    plt.contour(log_KOA, log_KAW, Phi_soil, levels=[0.1, 0.5], colors='black', alpha=0.5)  # Phi_water contours

    scatter = plt.scatter(df['log(Koa)'], df['log(Kaw)'], c=(df['log(Koc) (L/kg)']), cmap='inferno', s=100)

    # Add color bar to indicate log(Kaw) values
    plt.colorbar(scatter, label='log(Koc)  (L/Kg)')

    # Annotate each compound on the plot
    [plt.text(df['log(Koa)'][i], df['log(Kaw)'][i], df['Compound'][i], fontsize=9, ha='right') for i in range(len(df))]

    # Label the axes
    plt.xlabel('log(Koa)')
    plt.ylabel('log(Kaw)')
    plt.title('Chemical Space Plot (CSP) of the chemicals of interest.')

    # Show grid lines
    plt.grid(True)

    xlim_min = float(input(f"Minimum log(Koa) to display: "))
    xlim_max = float(input(f"Maximum log(Koa) to display: "))

    ylim_min = float(input(f"Minimum log(Kaw) to display: "))
    ylim_max = float(input(f"Maximum log(Kaw) to display: "))

    ax = plt.gca()
    ax.set_xlim([xlim_min, xlim_max])
    ax.set_ylim([ylim_min, ylim_max])


    # Display the plot
    print("Compound table:")
    print(df)
    print(f"Volume of air: {Va} m^3\nVolume of water: {Vw} m^3\nVolume of soil/organics: {Vom} m^3\n")
    print("The lines represent 0.90 fraction in the phase, while colour borders represent a 0.50 fraction.\nYou can hover over the point on the plot to see the (x,y) coordinates on the bottom right.")
    plt.show()

except csv.Error:
    print("Could not read .csv file. Please make sure to type the name to the file (\"example.csv\") and that the file is in the same folder.")
except FileNotFoundError:
    print(f"Could not find {csv_path}")