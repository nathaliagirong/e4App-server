import csv
import sampen
import nolds
import numpy as np
import pandas as pd
import heartpy as hp
import matplotlib.pyplot as plt
import math
import neurokit as nk
import pywt
from pywt import *
from math import *
from heartpy import *
from scipy import signal
from scipy.signal import *
from pylab import *
from hrvanalysis import *
#from entropy import spectral_entropy
#from fractions import Fraction as frac
from sklearn.externals import joblib
import xgboost as xgb

sign = np.genfromtxt('./controllers/file.csv', dtype="float", delimiter=",")

sign2 = sign[0:3840]

def resamp_interp(signal, input_fs, output_fs):
    
    scale = output_fs / input_fs
    # calculate new length of sample
    n = round(len(signal) * scale)

    resampled_signal = np.interp(
        np.linspace(0.0, 1.0, n, endpoint=False),  # where to interpret
        np.linspace(0.0, 1.0, len(signal), endpoint=False),  # known positions
        signal,  # known data points
    )
    return resampled_signal

sigR = resamp_interp(sign2, 64, 128)

max_D = max(sigR)

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

lowcut = 0.5
highcut = 45
fs = 128
num_datos = len(sigR)
T = 0.0078125
nsamples = num_datos

t = np.linspace(0, T, nsamples, endpoint=False)

y = butter_bandpass_filter(sigR, lowcut, highcut, fs, order=3)

max_Y= max(y)

Y_ord = sort(y)

p90Y = np.percentile(Y_ord, 88)

y[y>p90Y]=max_Y

peaks, _ = find_peaks(y, height=p90Y)

RRin = diff(peaks)

TimeDF = get_time_domain_features(RRin)

LinearDF = get_poincare_plot_features(RRin)

Media = TimeDF['mean_nni']

std = std(RRin)

def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation."""
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))

MAD = mad(RRin)

mean_rr_interval=sum(RRin)/len(RRin)   
square_dstnceA=(np.transpose(RRin))
square_dstnce = np.power(square_dstnceA,2)
avg_square_dstnce=sum(square_dstnce)/len(square_dstnce)
RMSSD2=math.sqrt(avg_square_dstnce)

SD1 = LinearDF['sd1']
SD2 = LinearDF['sd2']

SDRR = np.std(RRin)

S=(pi*SD1*SD2) 

fs = 128
n = 10*len(sigR)
f = range(128)
fnew = resamp_interp(f, 1, 60)
FFT_sig = fft(sigR, len(sigR))
FFT = np.fft.fftshift(FFT_sig)
FFT_pos = abs(FFT)

peaks, _ = find_peaks(FFT_pos)

p_int = diff(peaks)

SpEnt = nk.complexity_entropy_spectral(FFT_pos, 128)

(cA, cD) = pywt.dwt(sign, 'db1', mode = 'sym')

AV_cA = absolute(cA)
AV_cD = absolute(cD)

mean_cA = mean(AV_cA)

p_cD = float_power(AV_cD, 2)

EP_cD = sum(p_cD)

std_cA = np.std(cA)



features=[]
features = [Media,std,MAD, RMSSD2,SD1,SDRR,S,SpEnt,mean_cA,EP_cD,std_cA]
#print('Features: ',features)

model = joblib.load('./controllers/XGBClassifier_G3_VFinal.pkl') 

preds = model.predict(features)
#print('Classificación: ',preds)

if preds == 1.:
    print('true')
else:
    print('false')



