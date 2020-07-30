# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import MySQLdb as dbapi
import time, os
import MySQLdb.cursors as cursors
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

QUERY="SELECT * FROM mci.mci_opsformtable ORDER BY entry_date DESC;"
db=dbapi.connect(host='34.66.99.26',port=3306,user='ccdev',passwd='0041')

cur=db.cursor()
cur.execute(QUERY)
result=list(cur)
#print(result)
sqlresult=json.dumps(result, indent=4, sort_keys=True, default=str)
cleanresult=pd.DataFrame(result, columns=['employeeid', 'craneid', 'check1', 'check2', 'check3', 'check4', 'check5', 'check6', 'check7', 'check8', 'check9', 'check10', 'check11', 'check12', 'check13', 'check14', 'check15', 'check16', 'check17', 'check18', 'comments', 'entrydate', 'updatedate', 'inspstatus'])
data=pd.read_json(sqlresult)
df=pd.DataFrame(data)

"""df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})"""

fig = px.bar(df, x="inspstatus", y=df['inspstatus'].value_counts(), color="inspstatus", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)