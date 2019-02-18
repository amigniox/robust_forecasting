import datetime
import json

import boto3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from flask import Flask, render_template, request

matplotlib.use('agg')

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

PAGEVIEW_ADDR = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate'

with open('accessKeys.json') as f:
    id_key = json.load(f)

sagemaker = boto3.client('sagemaker-runtime', aws_access_key_id=id_key['ID'], aws_secret_access_key=id_key['key'], region_name='us-east-2')


@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['url'] == '':
            start = request.form['start']
            end = request.form['end']
            wiki_project = request.form['wiki_project']
            url = '{}/{}/{}/{}/{}'.format(PAGEVIEW_ADDR, wiki_project, 'all-access/all-agents/hourly', start, end)
        else:
            url = request.form['url']
        try:
            result = plot(url)
        except:
            return "Something bad happens, please check your url and make sure HTTP response has right format JSON"
    else:
        result = None
    print(result)
    return render_template('index.html', result=result)


def plot(url):
    response = requests.get(url)
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
        EndpointName='DEMO-deepar-2019-02-18-02-03-13-173',
        Body=req,
        ContentType='application/json',
        Accept='Accept'
    )

    ans = decode_response(res, prediction_time, False)

    images = []
    context_length = 118
    prediction_length = 48

    plt.figure()
    plt.style.use('dark_background')
    actual_series[:-context_length - prediction_length].plot(label='History')
    actual_series[-context_length - prediction_length:-prediction_length + 1].plot(label='Context')
    actual_series[- prediction_length:].plot(label='Target')
    plt.title('Input time series')
    ax1 = plt.gca()
    ax1.get_yaxis().get_major_formatter().set_scientific(False)
    ax1.set_facecolor('#2b2b2b')
    plt.legend()
    plt.savefig('static/images/fig1.png', facecolor='#2b2b2b')
    images.append('static/images/fig1.png')

    plt.figure()
    actual_series[-context_length-prediction_length:].plot(label='target', title='Target vs prediction: zoom in view')
    p10 = ans['0.1']
    p90 = ans['0.9']
    plt.fill_between(p10.index, p10, p90, color='y', alpha=0.5, label='80% confidence interval')
    ans['0.5'].plot(label='prediction median')
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_facecolor('#2b2b2b')
    lg = plt.legend()
    lg.get_frame().set_facecolor('#2b2b2b')
    plt.savefig('static/images/fig2.png', facecolor='#2b2b2b')

    images.append('static/images/fig2.png')
    return images


def series_to_dict(ts, cat=None, dynamic_feat=None):
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

@application.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    application.debug = True
    application.run()

