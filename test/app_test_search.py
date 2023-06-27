from dash import Dash, dcc, html, callback, Output, Input, State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from fast_autocomplete import AutoComplete

import sys
sys.path.append('/Users/tushevg/Desktop/syndive')
import layouts.dbtools as db

df_info = db.tableToDataFrame('info', 'data/mpibr_synprot.db')
ac_info = db.infoToAutoComplete(df_info)

app = Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div([
    dmc.Group([
        dmc.Select(id='search-bar', 
                    placeholder='Search gene or protein',
                    data=[],
                    searchable=True,
                    limit=20,
                    clearable=True,
                    icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal')),
        dmc.Text("selected", id='selected-value', size='xl')
    ])
    
],style={"alignItems": "center"})


@app.callback(Output("search-bar", "data"),
          Input("search-bar", "searchValue"))
def search_value(searchValue):
    list = db.matchAutoComplete(searchValue, ac_info)
    if (len(list) > 0):
        return list
    else:
        raise PreventUpdate


@callback(Output("selected-value", "children"),
          Input("search-bar", "value"))
def select_value(value):
    if not value:
        raise PreventUpdate
    key = db.keyAutoComplete(value, ac_info)
    return key



if __name__ == '__main__':
    app.run_server(debug=True)