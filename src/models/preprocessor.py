import datetime
import requests
import json


def save_json(start, end, path):
    start_date = datetime.datetime.strptime(start, '%Y%m%d')
    end_date = datetime.datetime.strptime(end, '%Y%m%d')
    if (end_date - start_date).days < 0:
        raise Exception('start date should NOT after end date')

    # wiki all projects' page views by human (not web scraping) per hour on a day
    base_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/all-projects/all-access/user/hourly/'
    data = dict()
    data['start'] = start + '00'
    data['target'] = []
    delta = datetime.timedelta(days=199)
    x = 1
    while start_date <= end_date:
        print('<-----iteration ' + str(x) + ' starts----->')
        if start_date + delta <= end_date:
            final_url = base_url + start_date.strftime('%Y%m%d') + '00/' + (start_date + delta).strftime('%Y%m%d') + '23'
        else:
            final_url = base_url + start_date.strftime('%Y%m%d') + '00/' + end + '23'
        print (final_url)  # debug
        # use wiki api to get an hourly timeseries of all project's pageviews belonging to human users from start date
        # to end date
        r = requests.get(final_url)
        r.raise_for_status()
        output = r.json()
        print('processed data points: ' + str(len(output['items'])))  # debug
        for i in range(len(output['items'])):
            data['target'].append(output['items'][i]['views'])
        start_date += datetime.timedelta(days=200)
        x += 1

    with open(path, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))


save_json('20151001', '20181201', 'data.json')
