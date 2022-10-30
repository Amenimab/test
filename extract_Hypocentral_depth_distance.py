from decimal import Decimal
import os

from ast import Slice
import pandas as pd
import numpy as np
from numpy.fft import fft, fftfreq
from scipy.fft import ifft
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from math import *


list_fichier = os.listdir( )
#print(list_fichier)
list_tra = []
for i in range(0, len(list_fichier)):
    if '.TRA' in list_fichier[i]:
        list_tra.append(list_fichier[i])

depth_list = []
distance_list =[]
acceleration_max_list = []
nombre_cycles_list = []

for file_name in list_tra :
    file = open(file_name)
    lines = file.readlines()
    
    ####################
    ### EXTRACT DEPTH ##
    ####################
    depth = Decimal(lines[5].split(  )[-1])
    depth_list.append(depth)
    #print("Depth ?? ", depth)

    #######################
    ### EXTRACT DISTANCE ##
    #######################    
    distance = Decimal(lines[7].split()[-2])
    distance_list.append(distance)
    #print("Distance ??", distance)

    ###############################
    ### EXTRACT MAX ACCELERATION ##
    ###############################
    end_line_index = 0
    for i in range(40,60):
        if lines[i] == "END_HEADER\n" :
            #print(i)
            end_line_index = i
    #print(lines[end_line_index])

    # csv_name = file_name[:4] + file_name[20:-8] + file_name[-7:-4] + "A" + ".csv"
    # #print(csv_name)
    # open(csv_name, "a").write("acceleration,pas_du_temps\n")

    acceleration_lines = lines[end_line_index+3:]
    pas_du_temps = 0
    liste_des_accelerations =[]
    for acceleration_line in acceleration_lines :
        acceleration_line_list = (acceleration_line.split("  "))
        acceleration = acceleration_line_list[-1]
        acceleration_final = acceleration[:-1]
        #print(acceleration_final)
        if acceleration_final == "" :
            # print(".")
            acceleration_final = acceleration_line_list[-3]
            # print(acceleration_final)
        acceleration_final = float(acceleration_final)
        liste_des_accelerations.append(acceleration_final)
        # open(csv_name, "a").write(acceleration_final + "," + str(pas_du_temps) + "\n")
        # pas_du_temps = pas_du_temps + 1/sampling_rate
    liste_des_accelerations
    acc_max = max(liste_des_accelerations)
    acceleration_max_list.append(acc_max)

    ################################
    ### EXTRACT NOMBRE DE CYCLE  ###
    ################################ 
    csv_name = file_name[:4] + file_name[20:-8] + file_name[-7:-4] + "A" + ".csv"
    np.seterr(divide='ignore', invalid='ignore')
    a=pd.read_csv(csv_name,usecols=[0])
    b=pd.read_csv(csv_name,usecols=[1])
    n=len(a)
    dt=0.025 #time increment in each data
    acc=a.values.flatten()*9.81 #to convert DataFrame to 1D array
    Temps=b.values.flatten() #to convert DataFrame to 1D array
    #acc & Time values must be in numpy array format for half way mirror calculation
    ampf=fft(acc)*dt
    freq=abs(fftfreq(n,d=dt))
    FFT=abs(ampf.real)
    Acc_fourier = ifft(ampf/dt).real/9.81
    N = 3 #Ordre du filtre
    w = (2*pi)*freq #acc circulaire
    FREQ_LP = 16.66
    FREQ_HP = 0.3
    FILTER_LP = np.power(1/(1+np.power((freq/FREQ_LP),2*N)),1/2)
    FILTER_HP = np.power(np.power(freq/FREQ_HP,2*N)/(1+np.power(freq/FREQ_HP,2*N)),1/2)
    Fourier_filtré = ampf*FILTER_LP*FILTER_HP 
    Acc_filtrée = ifft(Fourier_filtré/dt).real/9.81
    V = np.nan_to_num(Fourier_filtré/w)
    D = np.nan_to_num(Fourier_filtré/(w*w))
    Vitesses = ifft(V/dt).real
    Déplacements = ifft(-D/dt).real
    #Peak counting
    # Threshold value (for height of peaks and valleys)
    thresh = 0.1*np.amax(abs(Acc_filtrée))
    # Find indices of peaks
    peak_idx, _ = find_peaks(Acc_filtrée, height=thresh)
    # Find indices of valleys (from inverting the signal)
    valley_idx, _ = find_peaks(-Acc_filtrée, height=thresh)
    #Ti = np.append(Temps[peak_idx],Temps[valley_idx])
    Ui = np.append(Acc_filtrée[peak_idx],Acc_filtrée[valley_idx])
    N_eq = (1/2)*sum(np.power(abs(Ui)/(0.65*max(abs(Ui))),1/0.337))
    nombre_cycles_list.append(N_eq)

    # print("file_name ", file_name)
    # print("depth", depth)
    # print("Distance", distance)
    # print("Acceleration_max", acc_max)
    # print("csv_name", csv_name)
    # print('Le nombre de cycles equivalent (Boulanger et Idriss) :', N_eq)
    # print("-------------------------------------------------")

# print("len depth list", len(depth_list))
# print("distance list", len(distance_list))
# print("acceleration_max list", len(acceleration_max_list))
# print("nombre cycles max", len(nombre_cycles_list))


##############
#### PLOT ####
##############

# plot nombre de cycles en fonction de l'acc max
fig1 = plt.figure(1)
plt.scatter(acceleration_max_list, nombre_cycles_list)
plt.title("Nombre de cycles en fonction de l'acceleration maximale")
plt.xlabel("Acceleration")
plt.ylabel("Nombre de cycles")
# plt.legend()


# plot nombre de cycles en fonction de la distance 
fig2 = plt.figure(2)
plt.scatter(distance_list, nombre_cycles_list)
plt.title("Nombre de cycles en fonction de la distance")
plt.xlabel("Distance")
plt.ylabel("Nombre de cycles")

#plt.show()


####################
### SAVE 2 FILES ###
####################

# Nombre de cycles en fonction de l'acc max :
file_name1 = "nombre_cyles_acc_max.csv"
open(file_name1, "a").write("acc max,nombre_cycles\n")
for i in range(len(acceleration_max_list)):
    open(file_name1, "a").write(str(acceleration_max_list[i]))
    open(file_name1, "a").write(",")
    open(file_name1, "a").write(str(nombre_cycles_list[i]))
    open(file_name1, "a").write("\n")

# Nombre de cycles en fonction de l'acc max :
file_name2 = "nombre_cyles_distance.csv"
open(file_name2, "a").write("distance,nombre_cycles\n")
for i in range(len(acceleration_max_list)):
    open(file_name2, "a").write(str(distance_list[i]))
    open(file_name2, "a").write(",")
    open(file_name2, "a").write(str(nombre_cycles_list[i]))
    open(file_name2, "a").write("\n")


