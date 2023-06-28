from dash import Dash, dcc, html, callback, Output, Input, State, ctx, ALL
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from fast_autocomplete import AutoComplete
import pandas as pd

import sys
sys.path.append('/Users/tushevg/Desktop/syndive')

import layouts.dbtools as db
from layouts.header import header
from layouts.footer import footer

## --- HELPER FUNCTIONS --- ###
def table_body(df: pd.DataFrame) -> html.Tbody:
    df = df.sort_values('gene')
    rows = []
    for key, row in df.iterrows():
        protein = html.Td(dmc.Anchor(dmc.Text(key, align='center'), href=f"https://www.uniprot.org/uniprotkb/{key}/entry"))
        gene = html.Td(dmc.Text(row['gene'], align='center'))
        product = html.Td(dmc.Text(row['product'], align='center', size='sm'))
        action_icon = dmc.ActionIcon(DashIconify(icon="mdi:remove", width=24),
                                                   id={'type':'remove-button', 'index':key}, variant='subtle', color='red', size='sm')
        action = html.Td(dmc.Center(action_icon))
        rows.append(html.Tr([protein, gene, product, action]))

    return html.Tbody(rows, id='table-body')

def table_create(df: pd.DataFrame) -> dmc.Table:
    header = html.Thead(html.Tr([html.Th(dmc.Text('protein', align='center')),
                    html.Th(dmc.Text('gene', align='center')),
                    html.Th(dmc.Text('product', align='center')),
                    html.Th(dmc.Text('edit', align='center'))]), id='table-header')
    body = table_body(df)
    return dmc.Table(id='table-info',
                    verticalSpacing="sm",
                    horizontalSpacing="sm",
                    highlightOnHover=True,
                    children=[header, body])


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto"
]

app = Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)


### --- ALLOCATE DATA --- ###
db_file = 'data/mpibr_synprot.db'
query_list = ['Gad1', 'Gad2', 'Dlg4', 
               'Shank1', 'Psmc1', 'Psmd5', 'Psma7',
               'Psmc2', 'Th']
df_info = db.listToDataFrame(search_list=query_list, db_column='gene',
                             db_table='info', db_file=db_file)
df_enriched = db.listToDataFrame(search_list=df_info.index.to_list(), 
                                 db_column='protein', db_table='enriched', db_file=db_file)
df_expressed = db.listToDataFrame(search_list=df_info.index.to_list(), 
                                  db_column='protein', db_table='expressed', db_file=db_file)
df_info_full = db.tableToDataFrame(db_table='info', db_file=db_file)
ac_info = db.infoToAutoComplete(df_info=df_info_full)


### --- LAYOUT --- ###
app.layout = html.Div([
    dcc.Store(id='df-info', data=df_info.to_json()),
    dcc.Store(id='df-enriched', data=df_enriched.to_json()),
    dcc.Store(id='df-expressed', data=df_expressed.to_json()),
    dcc.Store(id='selected-key', storage_type='memory'),
    header(),
    html.Div(className='section',
                    id='dashboard',
                    children=dmc.Stack([table_create(df_info),
                    dmc.Text('Debug', id='id-debug', size='xl'),
                    dmc.Button('TEST', id='button-test')],
                            align='center', justify='center', spacing='xl')),
    ]
)


## --- test remove callback --- ##
@app.callback(
    [Output('id-debug', 'children'),
     Output('table-info', 'children'),
     Output('df-info', 'data')
    ],
    Input({'type':'remove-button', 'index': ALL}, "n_clicks"),
    State('df-info', 'data')
)
def handle_action_icon_clicks(n_clicks, df_info_data):
    clicked_id = ctx.triggered_id["index"]
    df_info = pd.read_json(df_info_data)
    df_info = df_info.drop(clicked_id)
    
    return (clicked_id, 
            table_create(df_info),
            df_info.to_json())




# ## ---
# ## update search list based on auto complete
# ## ---
# @app.callback(Output("search-term", "data"),
#           Input("search-term", "searchValue"))
# def search_value(searchValue):
#     list = db.matchAutoComplete(searchValue, ac_info)
#     if (len(list) > 0):
#         return list
#     else:
#         raise PreventUpdate


# ## ---
# ## select a value from search list
# ## ---
# @callback(Output("selected-key", "data"),
#           Input("search-term", "value"))
# def select_value(value):
#     if not value:
#         raise PreventUpdate
#     key = db.keyAutoComplete(value, ac_info)
#     db.updateInfoCount(key=key, 
#                        db_column='count', 
#                        db_key_column='protein',
#                        db_table='info',
#                        db_file=db_file)
#     return key


# @app.callback(
#     Output('id-debug', 'children'),
#     Input({'type': 'remove-button', 'index': 'ANY'}, 'n_clicks'),
#     State('table-data', 'children')
# )
# def update_data(clicked_button, current_rows):
#     action_id = triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     return html.Div(dmc.Text(action_id))
#     # if action_id == 'selected-key':
#     #     return html.Div(dmc.Text(key))
#     # else:
#     #     for key, row in df_info.iterrows():
#     #         if action_id == 'id-'+key:
#     #             return html.Div(dmc.Text(key))


if __name__ == '__main__':
    app.run_server(debug=True)