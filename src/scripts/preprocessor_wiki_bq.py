"""
Pre-process json lines downloaded from Google BigQuery table.
Output file as a different json lines format that DeepAR can consume.
"""
import json
import datetime

data = []
with open('2017.json') as f:
    for line in f:
        data.append(json.loads(line))
ans = []


start_date = datetime.datetime.strptime('20170101 00:00:00', '%Y%m%d %H:%M:%S')
end_date = datetime.datetime.strptime('20171231 00:00:00', '%Y%m%d %H:%M:%S')
hour = datetime.timedelta(hours=1)
zero = datetime.timedelta(hours=0)

n = len(data)
i = 0
while i < n:
    temp = dict()
    title = data[i]['title']
    temp['start'] = '2017-01-01 00:00:00'
    temp['target'] = []
    exp_date = start_date - hour
    bad_points = 0
    while i < n and data[i]['title'] == title:
        curr_time = datetime.datetime.strptime(data[i]['datehour'][:-4], '%Y-%m-%d %H:%M:%S')
        while curr_time - exp_date > hour:
            temp['target'].append(None)
            bad_points += 1
            exp_date += hour
        temp['target'].append(int(data[i]['views']))
        exp_date = curr_time
        i += 1
    while (end_date - exp_date) > zero:
        temp['target'].append(None)
        bad_points += 1
        exp_date += hour
    if bad_points / 8737 < 0.7:
        if len(temp['target']) == 8737:
            ans.append(temp)
        if len(temp['target']) == 8738:
            temp['target'] = temp['target'][:-1]
            if len(temp['target']) == 8737:
                print("here")
                ans.append(temp)

with open("big_train.json", 'w') as outfile:
    outfile.write('\n'.join(json.dumps(i) for i in ans) + '\n')


