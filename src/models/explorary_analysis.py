import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

#data_location = "s3://{}/test/test.json".format(s3_data_path)
data_location = 'train.json'
df_ts = pd.read_json(data_location, lines = True)

num_pt = len(df_ts.iloc[1, 1])
num_ts = len(df_ts)
freq = 'H'

time_series_wiki = []
for k in range(num_ts):
    t0 = df_ts.iloc[k, 0]
    data = df_ts.iloc[k, 1]
    index = pd.DatetimeIndex(start=t0, freq=freq, periods=num_pt)
    time_series_wiki.append(pd.Series(data=data, index=index))


for k in range(len(list_of_wiki_pred)):
    plt.figure(figsize=(12,6))
    time_series_wiki[k][-prediction_length-context_length:].plot(label='target')
    #p10 = list_of_wiki_pred[k]['0.1']
    #p90 = list_of_wiki_pred[k]['0.9']
    #plt.fill_between(p10.index, p10, p90, color='y', alpha=0.5, label='80% confidence interval')
    #list_of_wiki_pred[k]['0.5'].plot(label='prediction median')
    plt.legend()
    plt.show()
