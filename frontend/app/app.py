#!/usr/bin/env python
from datetime import datetime
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import trino

# connect to trino
cur = trino.dbapi.connect(
    host = 'trino',
    port = 8080,
    user = 'user'
).cursor()

NOMBRE_APP = 'Pedidos - RAH'
TITULO = 'Pedidos 🍔'
FREQ_UPDATE = 3  # en segundos
QUERY = 'SELECT burger, name, time FROM mongodb.rah.pedidos ORDER BY time DESC'
COLUMNAS = ['Hamburguesa', 'Pedido', 'Hora']

#############################################################
# creditos del favicon: iconos8.es

style_header = {
    'backgroundColor': '#009879',
    'color': '#FFFFFF',
    'padding': '20px',
    'fontSize': 28,
    'border': '5',
    'textAlign' : 'center',
}
style_cell = {
    'backgroundColor': '#FFFFFF',
    'color': '#000000',
    'fontSize': 20,
    'font-family': 'sans-serif',
    'padding': '20px',
    'paddingLeft' : '50px',
    'paddingRight' : '50px',
    'border': 'thin solid #FFFFFF',
    'textAlign' : 'center',
    'borderBottom' : '1px solid #DDDDDD',
}

style_data_conditional = [
    {'if': {'row_index': 'odd'}, 'backgroundColor': '#f3f3f3'},
    {'if': {'column_editable': 'False'}, 'cursor': 'not-allowed'}
]

style_table = {'borderRadius': '10px', 'overflow': 'hidden'}
center_style = {'width' : '100%', 'display': 'flex', 'justifyContent': 'center'}
basic_style = {'textAlign': 'center', 'margin': '5%'}

#############################################################

app = Dash(__name__, title=NOMBRE_APP, update_title=None)

app.layout = html.Div([
    html.Div(TITULO, className='app-header'),
    html.Div(style={'padding':'15px'}),
    html.Div(id='table',style=center_style),
    html.Div(id='tbl_out'),
    dcc.Interval(id='interval-component', interval=FREQ_UPDATE*1000, n_intervals=0)],
    style=basic_style,
    id='main-body'
)

@app.callback(Output('table', 'children'), [Input('interval-component', 'n_intervals')])
def update(n_intervals):
    cur.execute(QUERY)
    rows = cur.fetchall()

    res = []
    for row in rows:
        newRow = []
        for result in row:
            if isinstance(result, datetime):
                newRow.append(result.strftime("%H:%M - %d/%m/%Y"))
            elif isinstance(result, str):
                newRow.append(result.capitalize())
            else: newRow.append(result)
        res.append(newRow)

    df = pd.DataFrame.from_records(res, columns=COLUMNAS)
    return [ dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_header=style_header,
                style_cell=style_cell,
                style_data_conditional=style_data_conditional + 
                    [{'if': {'row_index': len(rows)-1}, 'borderBottom' : '2px solid #009879'}],
                style_table=style_table,
                fill_width=True,
                id='burger-table',
                editable=False,
                cell_selectable=False,
                row_deletable=True
            )
    ]

@app.callback(
    Output('tbl_out', 'children'),
    [Input('burger-table', 'data_timestamp')],
    [State('burger-table', 'data'), State('burger-table', 'data_previous')])
def delete(_,current,previous):
    if previous is not None:
        for row in current: previous.remove(row)    # OJO: no puedo usar sets porque pueden haber filas iguales
        for row in previous:                        # Solo queda lo eliminado
            burger = str(row['Hamburguesa']).strip().lower()
            name   = str(row['Pedido']).strip().lower()
            cur.execute(f"SELECT CAST(_id AS VARCHAR) FROM mongodb.rah.pedidos WHERE burger='{burger}' AND name='{name}' ORDER BY time ASC LIMIT 1")
            id = cur.fetchall()[0][0]
            cur.execute(f"DELETE FROM mongodb.rah.pedidos WHERE _id=ObjectId('{id}')")
    update(-1)
    return ''


#############################################################

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8051)
