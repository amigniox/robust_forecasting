import pandas as pd
import glob as glob
import datetime as dt
import matplotlib.pyplot as plt
import os as os
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
from fbprophet import Prophet
data_path = "/Users/Robby/dev/insight_project/bottomless_coffee/data/"
file_names = glob.glob(data_path + "/*.csv")
data = {}
for file in file_names:
    df = pd.read_csv(file)
    data_names = file.split(' ')
    data.update({data_names[2]:df})
for key in data:
    for column in data[key]:
        try:
            data[key][column] = pd.to_datetime(data[key][column],format = '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            pass
user_id_list= pd.unique(data['sensorrecords']['user_id'])
data['orders'] = data['orders'][data['orders'].date_fulfilled.notnull()]
data['orders'] = data['orders'][data['orders'].date_fulfilled > dt.datetime(2014,1,1)]
c = []
data['orders'] = pd.merge(left=data['orders'], right=data['products'][['product_id', 'size']], on = 'product_id')
data['sensorrecords'] = data['sensorrecords'].sort_values(by='timestamp')
os.chdir("/Users/Robby/dev/insight_project/bottomless_coffee/gr/")
#keep this, in line 39 you will switch this back from a specific user_id to # i
#for i in user_id_list:
user_subset = (data['sensorrecords'].loc[(data['sensorrecords'].user_id == '5acff32aeebb8900148011a3')])
arima_subset = pd.Series(user_subset['adjusted_weight'].values , index=user_subset['timestamp'])
model = ARIMA(arima_subset, order=(3, 0, 0))
results_ARIMA = model.fit(disp=0)
output = results_ARIMA.forecast()
print(results_ARIMA.summary())
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.plot_date(user_subset['timestamp'],user_subset['adjusted_weight'], linestyle='solid')
plt.show()
plt.close()