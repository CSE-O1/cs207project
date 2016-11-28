import math
import numpy.fft as nfft
import numpy as np
import ArrayTimeSeries as ts
from scipy.stats import norm
import matplotlib.pyplot as plt

"""
Implementation of timeseries distance by kernel correlation

Contain functions to:
1. Standardize the time series (subtract the mean and divide by the standard deviation)

2. Calculate the cross-correlation

3. Compute the kernelized cross-correlation.

4. Compute the real distance between two timeseries


"""
def tsmaker(m, s, j):
    "generate timeseries for testing"
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return ts.ArrayTimeSeries(v, t)

def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts.ArrayTimeSeries(v, t)

def stand(x, m, s):
    "standardize timeseries x my mean m and std deviation s"
    return ((x.values() - m) / s)

def ccor(ts1, ts2):
    "given two standardized time series, compute their cross-correlation using FFT"
    fourier_ts1 = nfft.fft(ts1)
    fourier_ts2 = nfft.fft(ts2)
    return (1/len(ts1)) * nfft.ifft(fourier_ts1 * np.conj(fourier_ts2)).real


def max_corr_at_phase(ts1, ts2):
    "check the max correlation with the kernelized cross-correlation"
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr


def kernel_corr(ts1, ts2, mult=1):
    """
    Purpose:
    Compute a kernelized correlation to get a real distance
    
    Kernel normalized by np.sqrt(K(x,x)K(y,y)) so that the correlation
    of a time series with itself is 1. 
    
    Default multiplier set to 1.
    
    Source: http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
    """
    ccorVal = ccor(ts1, ts2)
    
    Kxy = np.sum(np.exp(mult*ccorVal))
    Kxx = np.sum(np.exp(mult*ccor(ts1, ts1)))
    Kyy = np.sum(np.exp(mult*ccor(ts2, ts2)))
    
    return Kxy/np.sqrt(Kxx*Kyy)

def kcorr_dist(kxy):
    """
    #The higher the correlation, the lower is the distance between two timeseries. 
    #Source: http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
    """
    return (2 * (1 - kxy))

# to test if functions above work
if __name__ == "__main__":
    t1 = tsmaker(0.5, 0.1, 0.01)
    t2 = tsmaker(0.5, 0.1, 0.01)
    print(t1.mean(), t1.std(), t2.mean(), t2.std())
    plt.plot(t1.values())
    plt.plot(t2.values())
    plt.show()
    standts1 = stand(t1, t1.mean(), t1.std())
    standts2 = stand(t2, t2.mean(), t2.std())
    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print("index = ", idx, "max corr", mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=10)
    print(sumcorr)
    
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3)
    plt.plot(t4)
    plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=10)
    print('kernel corr= ', sumcorr)
    print ("distance", kcorr_dist(sumcorr))