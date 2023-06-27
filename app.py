from dash import Dash, dcc, html, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import pandas as pd
from fast_autocomplete import AutoComplete

from layouts.header import header
from layouts.footer import footer
from layouts.about import about
from layouts.publications import publications
from layouts.dashboard import dashboard
from layouts.exports import exports
import layouts.dbtools as db
from layouts.plots.plot_expressed import paper_expressed, plot_expressed, update_select_data
from layouts.plots.plot_enriched import paper_enriched, plot_enriched
from layouts.plots.plot_cytoscape import plot_cytoscape
from layouts.table import table


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto"
]

app = Dash(__name__, external_stylesheets=external_stylesheets)



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
    about(),
    publications(),
    dashboard(df_info, df_enriched, df_expressed),
    dmc.Center(paper_expressed(df_info, df_expressed)),
    dmc.Center(paper_enriched(df_info, df_enriched)),
    dmc.Center(plot_cytoscape()),
    exports(),
    footer()]
)


# ### --- CALLBACKS --- ###
@app.callback(Output("search-term", "data"),
          Input("search-term", "searchValue"))
def search_value(searchValue):
    list = db.matchAutoComplete(searchValue, ac_info)
    if (len(list) > 0):
        return list
    else:
        raise PreventUpdate


@callback(Output("selected-key", "data"),
          Input("search-term", "value"))
def select_value(value):
    if not value:
        raise PreventUpdate
    key = db.keyAutoComplete(value, ac_info)
    db.updateInfoCount(key=key, 
                       db_column='count', 
                       db_key_column='protein',
                       db_table='info',
                       db_file=db_file)
    return key


@app.callback(
    [
        Output('df-info', 'data'),
        Output('df-enriched', 'data'),
        Output('df-expressed', 'data')
    ],
    Input('selected-key', 'data'),
    State('df-info', 'data'),
    State('df-enriched', 'data'),
    State('df-expressed', 'data')
)
def update_data_frames(key, df_info_data, df_enriched_data, df_expressed_data):
    if not key:
        raise PreventUpdate
    
    # Convert the data frames from JSON back to pandas DataFrames
    df_info = pd.read_json(df_info_data)
    df_enriched = pd.read_json(df_enriched_data)
    df_expressed = pd.read_json(df_expressed_data)

    # check if key exists
    if key in df_info.index:
        raise PreventUpdate
    
    # skip if row limits reached
    if df_info.shape[0] == 10:
        raise PreventUpdate
    
    # find new rows
    df_key_info = db.termToDataFrame(search_term=key, db_column='protein', db_table='info', db_file=db_file)
    df_key_enriched = db.termToDataFrame(search_term=key, db_column='protein', db_table='enriched', db_file=db_file)
    df_key_expressed = db.termToDataFrame(search_term=key, db_column='protein', db_table='expressed', db_file=db_file)
    if df_key_info.empty:
        raise PreventUpdate
    
    # concatenate rows
    df_info = pd.concat([df_info, df_key_info])
    df_enriched = pd.concat([df_enriched, df_key_enriched])
    df_expressed = pd.concat([df_expressed, df_key_expressed])

    return (df_info.to_json(),
            df_enriched.to_json(),
            df_expressed.to_json())


@app.callback(
    Output('data-table', 'children'),
    Input('df-info', 'data')
)
def update_data_table(data):
    df_info = pd.read_json(data)
    table_html = table(df_info)
    return table_html


@app.callback(
        Output('plot-enriched', 'figure'),
        Input('df-enriched', 'data'),
        State('df-info', 'data')
)
def update_plot_enriched(df_enriched_data, df_info_data):
    df_enriched = pd.read_json(df_enriched_data)
    df_info = pd.read_json(df_info_data)
    return plot_enriched(df_info, df_enriched)


@app.callback(
        Output('select-term', 'data'),
        Input('df-info', 'data')
)
def update_plot_expressed_list(df_info_data):
    df_info = pd.read_json(df_info_data)
    return update_select_data(df_info)


@callback(Output('plot-expressed', 'figure'),
          Input('select-term', 'value'),
          State('df-expressed', 'data')
)
def select_value(key, df_expressed_data):
    df_expressed = pd.read_json(df_expressed_data)
    return plot_expressed(df_expressed, key)


if __name__ == '__main__':
    app.run_server(debug=True)
