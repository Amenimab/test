from ast import Slice
import pandas as pd
import numpy as np
from numpy.fft import fft, fftfreq
from scipy.fft import ifft
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from math import *

#from sklearn.neighbors import DistanceMetric

np.seterr(divide='ignore', invalid='ignore')

csv_name = '2002A16HHEA.csv'

a=pd.read_csv(csv_name,usecols=[0])
b=pd.read_csv(csv_name,usecols=[1])
n=len(a)
dt=0.025 #time increment in each data
# for i in a.values.flatten():
#     print(float(i)*9.81)
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

Ti = np.append(Temps[peak_idx],Temps[valley_idx])
Ui = np.append(Acc_filtrée[peak_idx],Acc_filtrée[valley_idx])

N_eq = (1/2)*sum(np.power(abs(Ui)/(0.65*max(abs(Ui))),1/0.337))


plot10 = plt.figure(10)
# Plot signal
plt.plot(Temps, Acc_filtrée)

# Plot threshold
plt.plot([min(Temps), max(Temps)], [thresh, thresh], '--')
plt.plot([min(Temps), max(Temps)], [-thresh, -thresh], '--')

# Plot peaks
plt.plot(Ti,Ui, 'r.')

plt.title("Détermination des pics")
plot7 = plt.figure(7)
plt.plot(Temps, Déplacements)
plt.plot([min(Temps), max(Temps)], [0, 0], '--')
plt.title("profil des Déplacements")
plot6 = plt.figure(6)
plt.plot(Temps,Vitesses)
plt.title("Profil des Vitesses")
plot5 = plt.figure(5)
plt.plot(Temps,Acc_filtrée)
plt.title("Accélération Filtrée")
plot4 = plt.figure(4)
plt.plot(freq,abs(Fourier_filtré/9.81))
plt.title("Fourier Filtré")
plt.yscale('log')
plt.xscale('log')
plt.gca().invert_xaxis()
plot3 = plt.figure(3)
plt.plot(freq,FILTER_HP, color ='red', label='High Pass Filter')
plt.plot(freq,FILTER_LP, color ='green', label='Low Pass Filter')
plt.legend(loc='upper left')
plt.title("Pass Filter")
plt.xscale('log')
plt.grid(True)
plot2 = plt.figure(2)
plt.plot(Temps,Acc_fourier)
plt.title("Accélération par Fourier réversible")
plot1 = plt.figure(1)
plt.plot(freq,FFT/9.81)
plt.title("SPECTRE DE FOURIER")
plt.yscale('log')
plt.xscale('log')
plt.gca().invert_xaxis()

print('Le nombre de cycles equivalent (Boulanger et Idriss) :', N_eq)


#plt.show()

