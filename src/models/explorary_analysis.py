import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

#data_location = "s3://{}/test/test.json".format(s3_data_path)
with open('wp.txt') as f:
    wp_list = f.read().splitlines()

data_location = '~/Desktop/Manifold/data_json/raw/http_count_marketplace_8000_2018-05-17_13_46_40.json'  # 'train.json'
df_ts = pd.read_json(data_location, lines=True)

num_pt = min(len(df_ts.iloc[1, 1]), 100000)
print('use first ', num_pt, ' points in a time series')
num_ts = len(df_ts)
freq = '5s'

prediction_length = 48
context_length = 72
week = 148
month = 720
year = 8760


time_series_wiki = []
for k in range(num_ts):
    t0 = df_ts.iloc[k, 0]
    data = df_ts.iloc[k, 1][:num_pt]
    index = pd.DatetimeIndex(start=t0, freq=freq, periods=num_pt)
    time_series_wiki.append(pd.Series(data=data, index=index))


def time_domain_analysis(ts, label, window_size):
    import time
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # straight up plot
    plt.figure(figsize=(12, 6))
    x.plot(label='wiki project: ' + label)
    plt.title('time series plot')
    plt.legend()
    plt.show()

    # autocorrelation
    plt.figure(figsize=(15, 5))
    pd.plotting.autocorrelation_plot(ts);
    plt.title('autocorrelation')

    # rolling average
    plt.figure(figsize=(12, 6))
    ts.rolling(window=window_size, center=False).mean().plot()
    plt.title('Rolling average')

    # rolling autocorrelation
    plt.figure(figsize=(12, 6))
    ts.rolling(window=window_size).corr(other=ts).plot()
    plt.title('Rolling autocorr')
