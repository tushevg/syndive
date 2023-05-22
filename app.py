from dash import Dash, dcc, html, callback, Output, Input, State

import dash_mantine_components as dmc
import pandas as pd
from fast_autocomplete import AutoComplete

from layouts.header import header
from layouts.footer import footer
from layouts.plot_enriched import plot_enriched
from layouts.plot_expressed import plot_expressd
from layouts.plot_cytoscape import plot_cytoscape
from layouts.about import about
from layouts.publications import publications
from layouts.dashboard import dashboard
from layouts.exports import exports


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto"
]

app = Dash(__name__, external_stylesheets=external_stylesheets)



### --- ALLOCATE DATA --- ###
db_file = 'data/mpibr_synprot.db'
query_list = ['Gad1', 'Gad2', 'Dlg4', 
               'Shank1', 'Psmc1', 'Psmd5', 'Psma7',
               'Psmc2', 'Th']
# df_info = dbquery_find_list(query_list, 'gene', 'info', db_file)
# df_enriched = dbquery_find_list(df_info['protein'].to_list(), 'protein', 'enriched', db_file)
# df_expressed = dbquery_find_list(df_info['protein'].to_list(), 'protein', 'expressed', db_file)


### -- CREATE ELMENTS PROTOTYPES --- ###
# #table_info = create_table_info(df_info)
# fig_enriched = plot_enriched(df_info, df_enriched)
# fig_expressed = plot_expressd(df_expressed, "Q62108")

### --- LAYOUT --- ###

app.layout = html.Div([
    dcc.Store(id='df-info', data=df_info.to_json()),
    dcc.Store(id='df-enriched', data=df_enriched.to_json()),
    dcc.Store(id='df-expressed', data=df_expressed.to_json()),
    header(),
    about(),
    publications(),
    dashboard(df_info, df_enriched, df_expressed),
    exports(),
    footer()]
)


# create_table_info(df_info),
# dmc.Paper(dmc.Stack([dmc.Center(dmc.Select(data=df_info['gene'].to_list(), id="select-term", value="Dlg4")),
# dcc.Graph(id='plot-expressed', figure=fig_expressed)]),
# style={"width": "90%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"},
# shadow="sm", withBorder=True),
# dmc.Paper(dcc.Graph(id='plot-enriched', figure=fig_enriched),
# style={"width": "90%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"},
# shadow="sm", withBorder=True)
# dmc.Paper(plot_cytoscape(),
# style={"width": "90%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"},
# shadow="sm", withBorder=True),  


# ### --- CALLBACKS --- ###

# # define a callback to update the dataframe        
# @callback(
#     [Output('df-info', 'data'),
#      Output('df-enriched', 'data'),
#      Output('df-expressed', 'data'),
#      Output('table-output', 'children'),
#      Output('plot-enriched', 'figure'),
#      Output('select-term', 'data')],
#     Input('search-term', 'n_submit'), # trigger
#     State('df-info', 'data'),
#     State('search-term', 'value'),
#     prevent_initial_call=True
# )
# def search_data(n_submit, data, search_term):
#     df = pd.read_json(data)
#     df_query = df[(df['protein'] == search_term) | 
#                   (df['gene'] == search_term)]
#     if df_query.empty:
#         df_query = dbquery_find_term(search_term, 'info', db_file)
#         if not df_query.empty:
#             df = pd.concat([df, df_query], ignore_index=True)
#     table_html = create_table_info(df)
#     df_enriched = dbquery_find_list(df['protein'].to_list(), 'protein', 'enriched', db_file)
#     df_expressed = dbquery_find_list(df_info['protein'].to_list(), 'protein', 'expressed', db_file)
#     return (df.to_json(), 
#             df_enriched.to_json(), 
#             df_expressed.to_json(),
#             table_html, 
#             plot_enriched(df, df_enriched),
#             df['gene'].to_list())

# @callback(Output('plot-expressed', 'figure'),
#           Input('select-term', 'value'),
#           State('df-info', 'data'),
#           State('df-expressed', 'data'),
#           prevent_initial_call=True
# )
# def select_value(value, data_info, data_expressed):
#     df_info = pd.read_json(data_info)
#     df_expressed = pd.read_json(data_expressed)
#     search_term = df_info['protein'].loc[df_info['gene'] == value].iloc[0]
#     return plot_expressd(df_expressed, search_term)


if __name__ == '__main__':
    app.run_server(debug=True)
