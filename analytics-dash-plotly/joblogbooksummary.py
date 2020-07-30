import httplib2

from apiclient import discovery
from google.oauth2 import service_account

import MySQLdb as dbapi
import time, os
import sys
import csv
import json
import pandas as pd
import MySQLdb.cursors as cursors


while True:
    QUERY="SELECT * FROM jobinfo.jobformentriestosheets WHERE formtype LIKE '%NEW%' ORDER BY timestamp DESC;"
    db=dbapi.connect(host='35.232.234.247',port=3306,user='lt2g47',passwd='1047')

    cur=db.cursor()
    cur.execute(QUERY)
    result=list(cur)
    #print(result)
    sqlresult=json.dumps(result, indent=4, sort_keys=True, default=str)
    cleanresult=pd.DataFrame(result, columns=None)
    data=pd.read_json(sqlresult)
    newsqlresult=pd.DataFrame(data)
    #print(cleanresult)

    

    SPREADSHEET_ID = '1xCJcy-QCFsHU11wbHdFFVIhnT9cLh8Ur86GF84FxhVM'
    RANGE_NAME = 'NewJobIso!A2:S'

    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]
    secret_file = os.path.join(os.getcwd(), 'client_secrets.json')

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)

    service = discovery.build('sheets', 'v4', credentials=credentials)

    values = sqlresult

    service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='RAW', body=dict(majorDimension='ROWS',values=cleanresult.T.reset_index().T.values.tolist())).execute()


    QUERY1="SELECT jobnumber, timestamp, priority, status, details, concat(client,', ', equipmentassetnumber,', ',equipmentfieldname,', ', scopeofwork) AS jobsummary FROM jobinfo.jobformentriestosheets ORDER BY jobnumber DESC;"
    db1=dbapi.connect(host='35.232.234.247',port=3306,user='lt2g47',passwd='1047')

    cur1=db1.cursor()
    cur1.execute(QUERY1)
    result1=list(cur1)
    #print(result)
    sqlresult1=json.dumps(result1, indent=4, sort_keys=True, default=str)
    cleanresult1=pd.DataFrame(result1, columns=None)
    data1=pd.read_json(sqlresult1)
    newsqlresult1=pd.DataFrame(data1)
    #print(cleanresult)


    

    SPREADSHEET_ID1 = '1xCJcy-QCFsHU11wbHdFFVIhnT9cLh8Ur86GF84FxhVM'
    RANGE_NAME1 = 'JobLogbookSummary!A2:F'

    scopes1 = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]
    secret_file1 = os.path.join(os.getcwd(), 'client_secrets.json')

    credentials1 = service_account.Credentials.from_service_account_file(secret_file1, scopes=scopes1)

    service1 = discovery.build('sheets', 'v4', credentials=credentials1)

    values1 = sqlresult1

    service1.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID1, range=RANGE_NAME1, valueInputOption='RAW', body=dict(majorDimension='ROWS',values=cleanresult1.T.reset_index().T.values.tolist())).execute()

    


    print('Sheet successfully Updated')

    time.sleep(1)

