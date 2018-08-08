# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Change the flow = to your personal google calendar api credentials stored on your local machine.
"""
Shows basic usage of the Google Calendar API.This was created from the basic quickstart.py for google calendar API.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import numpy as np
import pandas as pd

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/Users/aidenjohnson/Library/Mobile Documents/com~apple~CloudDocs/Thinkful/Gtimesheet/client_secret_thinkful.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
#now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
local_datetime = datetime.datetime.strptime("2018-07-22 08:00:00", "%Y-%m-%d %H:%M:%S")
result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
now=result_utc_datetime.isoformat()+'Z'

print('Getting the upcoming 30 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=30, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])
#print(events)

d = []
if not events:
    print('No upcoming events found.')
for event in events:
    c = np.asarray(event['summary'])
    a = (event['start'].get('dateTime',event['start']))[:10]
    p = datetime.datetime.strftime(datetime.datetime.strptime(a,'%Y-%m-%d'),'%B %d, %Y')
    xe =datetime.datetime.strptime(((event['end'].get('dateTime',event['end']))[11:16]),'%H:%M')
    xs =datetime.datetime.strptime(((event['start'].get('dateTime',event['start']))[11:16]),'%H:%M')
    b =(xe-xs)
    hours = int(b.seconds // (60 * 60))
    mins = int((b.seconds // 60) % 60)
    if hours == 1:
        h = hours
    else:
        h = mins/60
    at = 'Data Science'
    rt = '$25'
    tot = '$' + str(h * 25)
    d.append([p,c,at,rt,h,tot])
    #print(c)
    df=pd.DataFrame(d, columns=('Date', 'Item','Allocate Towards','Rate','Qty in Hours','Total'))
    df.to_csv('gtime_sheet.csv')
    #np.savetxt("gtime_sheet.csv", c, delimiter=",")
# [END]
