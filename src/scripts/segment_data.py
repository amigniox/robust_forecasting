import heapq
import numpy as np

"""
This function characterize any given time series. 
Basically it gives a score on the time series various aspects: trend, seasonality (if window = day, then seasonality =
halfDay, day, week, month), the strongest characteristic will be the aspect with highest score; and 'spike' if the time
series don't show any of the previous characteristics.

The input will be Pandas series (with index = timestamp, and value = time series value) and window which simply defines the 
unit (conversion between the desired cycle and the Nyquist frequency).

The output will be a list with 8 elements:
[trend score, half day score, day score, week score, month score, 'strongest characteristic', 
mean in time domain, standard deviation in time domain]


CAUTION: sloppy scientific computing hard-coding style...

For detailed demonstration of how it works, please see notebook 04-wiki-data-stats.ipynb
"""


def characterize_ts(ts, window):
    y = ts.values  # signal
    Fs = 1  # sampling rate, in our case let's use 1 Hour^-1
    n = len(y)  # length of the signal
    k = np.arange(n)
    T = n / Fs
    frq = k / T  # two sides frequency range
    # we only keep the positive frequency up to the Nyquist = 1/(2*dT), dT = sampling interval
    cycle = frq[range(1, int(n / 2))] * window  # one side frequency range

    Y = np.fft.fft(y) / n  # fft computing and normalization
    Y = Y[range(1, int(n / 2))]  # again, spectrum corresponding to the positive half
    yabs = np.abs(Y)

    # locate the largest 15 peaks, use them to characterise the time series
    indx = heapq.nlargest(15, range(len(yabs)), yabs.__getitem__)
    amp = heapq.nlargest(15, yabs)

    mean = yabs.mean()
    std = yabs.std()
    cyc_hday = 2.0
    cyc_day = cyc_hday / 2.0
    cyc_week = cyc_day / 7.0
    cyc_month = cyc_day / 30.0

    comp = lambda a, b: np.abs(a / b - 1) < 0.05
    ts_type = ['trend', 'halfDay', 'Day', 'Week', 'Month', 'spike']
    report_list = [0] * 8
    for counter, value in enumerate(indx):
        # define a peak in frequency domain
        if amp[counter] > (mean + 3 * std):
            amp_norm = (amp[counter] - mean) / std
            if cycle[value] < 0.01:
                # trend (increasing, decreasing, gaussian pulse)
                report_list[0] = max(amp_norm, report_list[0])
            elif comp(cycle[value], cyc_hday):
                report_list[1] = max(amp_norm, report_list[1])
            elif comp(cycle[value], cyc_day):
                report_list[2] = max(amp_norm, report_list[2])
            elif comp(cycle[value], cyc_week):
                report_list[3] = max(amp_norm, report_list[3])
            elif comp(cycle[value], cyc_month):
                report_list[4] = max(amp_norm, report_list[4])

    if sum(report_list[:4]) > 0:
        index = report_list[:4].index(max(report_list[:4]))
        report_list[5] = ts_type[index]
    else:
        report_list[5] = ts_type[-1:]

    report_list[-2] = y.mean()
    report_list[-1] = y.std()
    return report_list