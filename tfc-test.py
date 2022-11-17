import requests
import json
from datetime import datetime, timedelta

# main_url = 'https://app.terraform.io/api/v2/runs/run-tB1Yrv8xX4y5z4Av/policy-checks'

token = 'ENTER-TOKEN-HERE'

hdrs = {
    'accept': 'application/json',
    'Authorization': 'Bearer {}'.format(token)
}

# resp = requests.get(main_url,headers=hdrs)
# print(resp)
# print(resp.text)

# get a list of all workspaces in a org
URL1 = 'https://app.terraform.io/api/v2/organizations/<nameoforg>/workspaces'
resp = requests.get(URL1, headers=hdrs)
# print(resp.text)
x = json.loads(resp.text)
# print(type(x))
wps = []
for wp in x['data']:
    print(wp['id'])
    wps.append(wp['id'])

print(wps)

# get a list of the runs of the workspaces
formater = "%Y-%m-%dT%H:%M:%S.%fZ"
# strt = datetime.datetime(2022, 10, 1), 
# end  = datetime.datetime(2022, 11, 30)
url2 = 'https://app.terraform.io/api/v2/workspaces/'
for wp in wps:
    temp = url2+wp+'/runs'
    print(temp)
    resp = requests.get(temp, headers=hdrs)
    # print(resp.text)
    run_list = json.loads(resp.text)['data']
    for run in run_list:
        created = run['attributes']['created-at']
        # print(type(created))
        # print(created)
        timestamp = datetime.strptime(created, formater)
        # print(type(timestamp))
        # print(timestamp)
        # print(timestamp.date)

        delta = datetime.now() - timestamp
        run_list = []
        if delta.days <= 30:
            print(run['id'])
            run_list.append(run['id'])

        #TODO use List Policy Checks api call to see if there was any soft-failed
        url3 = 'https://app.terraform.io/api/v2/runs/'
        for run in run_list:
            temp = url3 + run + '/policy-checks'
            print(temp)
            resp =  requests.get(temp, headers=hdrs)
            print(resp.text)
            #TODO - looks like the resp has a list of policy check, investigate and finsih logic
            advisory_failed = json.loads(resp.text)['data']['attributes']['result']['advisory-failed']
            # policy_list = json.loads(resp.text)['data']['attributes']['result']['sentinel']['data']['sentinel-controls']['policies']
            # p_name = 'sentinel-controls/aws-guardrails'
            # for p in policy_list:
            #     if p['policy'] == p_name and p['result'] is False:
            #         print("!!!FOUND ONE!!!")
            #         print(wp, run)
            #         print()
            print('\n\n')
        

    exit()



# date_strt, date_end = datetime(2022, 10, 1), datetime(2022, 11, 30)
