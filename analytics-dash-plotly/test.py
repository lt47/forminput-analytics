def lets_go():
    QUERY="SELECT employee_id, crane_id, comments, entry_date, inspstatus FROM mci.mci_opsformtable WHERE inspstatus IS NOT NULL ORDER BY entry_date DESC;"
    db=dbapi.connect(host='34.66.99.26',port=3306,user='ccdev',passwd='0041')
    cur=db.cursor()
    cur.execute(QUERY)
    result=list(cur)
    sqlresult=json.dumps(result, indent=4, sort_keys=True, default=str)
    cleanresult=pd.DataFrame(result, columns=['employeeid', 'craneid',  'comments', 'entrydate', 'inspstatus'])
    data=pd.read_json(sqlresult)
    df=cleanresult
    dfg=df.groupby('inspstatus').count().reset_index()
    fig=px.bar(dfg, x="inspstatus", y="craneid", color="inspstatus", barmode="stack", width=60, height=500)
    layout = {'autosize': False, 'height': 500, 'width': 670}
    fig['layout'].update(layout)
    return html.Div(children=[
    html.H1(children='Operators\' Inspection Report'),
    
    html.Div(children=[
        html.Div(
            dcc.Graph(
                id='graph'
                )),
        html.Div(
            dcc.Graph(
                id='graph2'
                ))
        ], style={'align-items': 'center', 'display': 'flex', 'flex flow': 'row'}),

    html.H4(id='table', children='Table'),

    dcc.Interval(id='live-update', interval=1*30000, n_intervals=0)
    ])