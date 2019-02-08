import json

import matplotlib
import matplotlib.pyplot as plt
import boto3
import pandas as pd
import numpy as np
import datetime
import requests
import csv

from flask import Flask, render_template, request

matplotlib.use('agg')

application = Flask(__name__)

with open('accessKeys.csv', 'r') as f:
    reader = csv.reader(f)
    id_key = list(reader)

sagemaker = boto3.client('sagemaker-runtime', aws_access_key_id=id_key[1][0], aws_secret_access_key=id_key[1][1], region_name='us-east-2')


@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        result = plot(request.form['apiUrl'], request.form['start'], request.form['end'])
    else:
        result = None

    return render_template('index.html', result=result)


def plot(url, start, end):
    response = requests.get('https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/' + url + '/all-access/all-agents/hourly/' + start + '/' + end)
    response.raise_for_status()
    output = response.json()
    start = output['items'][0]['timestamp'][:-2]
    start_date = datetime.datetime.strptime(start, '%Y%m%d')
    s = start_date.strftime('%Y-%m-%d') + ' 00:00:00'
    time = pd.DatetimeIndex(start=s, freq='H', periods=len(output['items']))
    views = []
    for item in output['items']:
        views.append(item['views'])
    actual_series = pd.Series(data=views, index=time)
    pred_series = actual_series[:-48]
    prediction_time = pred_series.index[-1] + 1

    instance = series_to_dict(actual_series)
    configuration = {
        "num_samples": 100,
        "output_types": ["quantiles"],
        "quantiles": ["0.1", "0.5", "0.9"]
    }
    http_request_data = {
        "instances": [instance],
        "configuration": configuration
    }
    req = json.dumps(http_request_data).encode('utf-8')

    res = sagemaker.invoke_endpoint(
        EndpointName='DEMO-deepar-2019-02-08-14-54-24-202',
        Body=req,
        ContentType='application/json',
        Accept='Accept'
    )

    ans = decode_response(res, prediction_time, False)
    plt.figure()
    actual_series[-72-48:].plot(label='target')
    p10 = ans['0.1']
    p90 = ans['0.9']
    plt.fill_between(p10.index, p10, p90, color='y', alpha=0.5, label='80% confidence interval')
    ans['0.5'].plot(label='prediction median')
    plt.legend()
    plt.savefig('static/images/fig.png')
    return 'static/images/fig.png'


def series_to_dict(ts, cat=None, dynamic_feat=None):
    """Given a pandas.Series object, returns a dictionary encoding the time series.

    ts -- a Pandas.Series object with the target time series
    cat -- an integer indicating the time series category

    Return value: a dictionary
    """
    obj = {"start": str(ts.index[0]), "target": encode_target(ts)}
    if cat is not None:
        obj["cat"] = cat
    if dynamic_feat is not None:
        obj["dynamic_feat"] = dynamic_feat
    return obj


def encode_target(ts):
    return [x if np.isfinite(x) else "NaN" for x in ts]


def decode_response(response, prediction_time, return_samples):
    # we only sent one time series so we only receive one in return
    # however, if possible one will pass multiple time series as predictions will then be faster
    body = response['Body'].read()
    predictions = json.loads(body)['predictions'][0]
    prediction_length = len(next(iter(predictions['quantiles'].values())))
    prediction_index = pd.DatetimeIndex(start=prediction_time, freq='H', periods=prediction_length)
    if return_samples:
        dict_of_samples = {'sample_' + str(i): s for i, s in enumerate(predictions['samples'])}
    else:
        dict_of_samples = {}
    return pd.DataFrame(data={**predictions['quantiles'], **dict_of_samples}, index=prediction_index)


if __name__ == '__main__':
    application.debug = True
    application.run()


