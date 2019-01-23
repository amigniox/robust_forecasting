import datetime
import requests
import json

def save_json(start, end, path):
    s3filesystem = s3fs.S3FileSystem()
    start_date = datetime.datetime.strptime(start, '%Y%m%d')
    end_date = datetime.datetime.strptime(end, '%Y%m%d')
    if (end_date - start_date).days < 0:
        raise Exception('start date should NOT after end date')

    ########## provide wiki-project list here! #########
    with open('wp.txt') as f:
        wp_list = f.read().splitlines()

    # put dict of each domain to this list
    all_data = []

    delta = datetime.timedelta(days=199)

    for item in wp_list:
        # wiki all projects' page views by human (not web scraping) per hour on a day
        base_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/' + item + '/all-access/all-agents/hourly/'
        start_date = datetime.datetime.strptime(start, '%Y%m%d')

        # dict is used to save JSON of each domain
        data = dict()
        data['start'] = start_date.strftime('%Y-%m-%d') + ' 00:00:00'
        data['target'] = []

        while start_date <= end_date:
            if start_date + delta <= end_date:
                final_url = base_url + start_date.strftime('%Y%m%d') + '00/' + (start_date + delta).strftime('%Y%m%d') + '23'
            else:
                final_url = base_url + start_date.strftime('%Y%m%d') + '00/' + end + '23'
            print (final_url)  # debug
            # make a API request here!!!
            response = requests.get(final_url)
            try:
                response.raise_for_status()
                output = response.json()
                print('processed data points: ' + str(len(output['items'])))  # debug
                for i in range(len(output['items'])):
                    data['target'].append(output['items'][i]['views'])
            except requests.exceptions.HTTPError as e:
                print("Error: " + str(e))
                break
            start_date += datetime.timedelta(days=200)
        if data['target']:
            all_data.append(data)

    # convert all items in list to JSON and write to a file
    print('saving data')
    with s3filesystem.open(path, 'w') as outfile:
        outfile.write('\n'.join(json.dumps(i) for i in all_data) +'\n')