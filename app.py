from dash import Dash, dcc, html, callback, Output, Input, State, ctx, ALL
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import pandas as pd
from fast_autocomplete import AutoComplete
from urllib.parse import urlparse, urlunparse
import os
import json

from layouts.header import header
from layouts.footer import footer
from layouts.about import about
from layouts.publications import publications
from layouts.dashboard import dashboard
from layouts.exports import exports
import layouts.dbtools as db
from layouts.table import table_create
from layouts.plots import plot_boxplot, plot_dotplot, paper_boxplot, paper_dotplot, update_select_data, paper_cytoscape


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto"
]

url_custom_path = os.getenv('SYNDIVE_URLPATH', '')
if not url_custom_path.endswith('/'):
    url_custom_path = url_custom_path + '/'

app = Dash(__name__, 
           external_stylesheets=external_stylesheets, 
           prevent_initial_callbacks=True,
           requests_pathname_prefix=url_custom_path)
server = app.server
app.title = 'syndive'
    
# Modify the index_string property to include the GTM code
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-JVVZRMCR6P"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-JVVZRMCR6P');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


### --- ALLOCATE DATA --- ###
db_file = 'data/mpibr_synprot.db'
query_list = ['Gad1', 'Gad2', 'Slc32a1', 'Slc17a7',
               'Shank1', 'Syt2', 'Th']
df_info = db.listToDataFrame(search_list=query_list, db_column='gene',
                             db_table='info', db_file=db_file)
df_enriched = db.listToDataFrame(search_list=df_info.index.to_list(), 
                                 db_column='protein', db_table='enriched', db_file=db_file)
df_expressed = db.listToDataFrame(search_list=df_info.index.to_list(), 
                                  db_column='protein', db_table='expressed', db_file=db_file)
df_foldchange = db.listToDataFrame(search_list=df_info.index.to_list(),
                                   db_column='protein', db_table='foldchange', db_file=db_file)
df_info_full = db.tableToDataFrame(db_table='info', db_file=db_file)
ac_info = db.infoToAutoComplete(df_info=df_info_full)

# read cytoscape data
with open('data/cytoscape_info.json', 'r') as f:
    elements = json.loads(f.read())
cyto_nodes = elements['nodes']
cyto_edges = elements['edges']

### --- LAYOUT --- ###
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='df-info', data=df_info.to_json()),
    dcc.Store(id='df-enriched', data=df_enriched.to_json()),
    dcc.Store(id='df-expressed', data=df_expressed.to_json()),
    dcc.Store(id='df-foldchange', data=df_foldchange.to_json()),
    dcc.Store(id='selected-key', storage_type='memory'),
    header(),
    about(),
    publications(),
    dashboard(df_info),
    paper_boxplot(df_info, df_expressed),
    paper_dotplot(df_info, df_enriched),
    paper_cytoscape(cyto_nodes, cyto_edges, df_info),
    exports(),
    footer(),
    dcc.Download(id='download')]
)

# ### --- CALLBACKS --- ###

## ---
## update search list based on auto complete
## ---
@app.callback(
    Output("search-term", "data"),
    Input("search-term", "searchValue")
)
def search_term(searchValue):
    list = db.matchAutoComplete(searchValue, ac_info)
    if (len(list) > 0):
        return list
    else:
        raise PreventUpdate


## ---
## select a value from search list
## ---
@app.callback(
    Output("selected-key", "data"),
    Input("search-term", "value")
)
def select_term(value):
    if not value:
        raise PreventUpdate
    key = db.keyAutoComplete(value, ac_info)
    db.updateInfoCount(key=key, 
                       db_column='count', 
                       db_key_column='protein',
                       db_table='info',
                       db_file=db_file)
    
    return key


## ---
## update data frames based on selected gene or deleted row
## ---
@app.callback(
    Output('df-info', 'data'),
    Output('df-enriched', 'data'),
    Output('df-expressed', 'data'),
    Input('selected-key', 'data'),
    Input({'type':'remove-button', 'index': ALL}, 'n_clicks'),
    State('df-info', 'data'),
    State('df-enriched', 'data'),
    State('df-expressed', 'data')
)
def update_data_frames(key, n_clicks, df_info_data, df_enriched_data, df_expressed_data):

    # convert json to data.frame
    df_info = pd.read_json(df_info_data)
    df_enriched = pd.read_json(df_enriched_data)
    df_expressed = pd.read_json(df_expressed_data)

    # retrieve current trigger
    triggered_id = ctx.triggered_id

    if isinstance(triggered_id, str):
        if triggered_id != 'selected-key':
            raise PreventUpdate
        
        if not key:
            raise PreventUpdate
        
        if key in df_info.index:
            raise PreventUpdate
        
        if df_info.shape[0] == 15:
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
        
    else:
        triggered_key = triggered_id['index']
        if df_info.shape[0] == 1:
            raise PreventUpdate
        
        df_info = df_info.drop(triggered_key)
        df_enriched = df_enriched.drop(triggered_key)
        df_expressed = df_expressed.drop(triggered_key)
    
    df_info = df_info.sort_values('gene')

    return (df_info.to_json(),
            df_enriched.to_json(),
            df_expressed.to_json())


## ---
## update info dependent data
## ---
@app.callback(
    Output('table-info', 'children'),
    Output('select-term', 'data'),
    Output('select-term', 'value'),
    Output('select-cytoscape-term', 'data'),
    Output('select-cytoscape-term', 'value'),
    Input('df-info', 'data')
)
def update_plot_expressed_list(df_info_data):
    df_info = pd.read_json(df_info_data)
    select_data = update_select_data(df_info)
    select_term = df_info.index[0]
    return (table_create(df_info),
        select_data, select_term,
        select_data, select_term)


## ---
## update plot expressed figure
## ---
@app.callback(
    Output('plot-expressed', 'figure'),
    Input('select-term', 'value'),
    Input('select-abundance', 'value'),
    State('df-expressed', 'data'),
    State('df-foldchange', 'data')
)
def select_value(key, value, df_expressed_data, df_foldchange_data):
    df_boxplot = pd.read_json(df_expressed_data)
    label_yaxis = 'protein abundance'
    if value == 'fold-change':
        df_boxplot = pd.read_json(df_foldchange_data)
        label_yaxis = 'fold change [log2 sorted/unsorted]'
    return plot_boxplot(df_boxplot, key, label_yaxis)

  

## ---
## update plot enriched figure
## ---
@app.callback(
    Output('plot-enriched', 'figure'),
    Input('df-info', 'data'),
    State('df-enriched', 'data')
)
def update_plot_enriched(df_info_data, df_enriched_data):
    df_info = pd.read_json(df_info_data)
    df_enriched = pd.read_json(df_enriched_data)
    return plot_dotplot(df_info, df_enriched)



## ---
## export data frames to csv files
## ---
@app.callback(
    Output('download', 'data'),
    Input({'type':'export-button', 'index': ALL}, 'n_clicks'),
    State('df-info', 'data'),
    State('df-enriched', 'data'),
    State('df-expressed', 'data')
)
def export_info(n_clicks, df_info_data, df_enriched_data, df_expressed_data):
    if n_clicks == 0:
        PreventUpdate

    triggered_id = ctx.triggered_id['index']
    
    if triggered_id == 'export-info':
        df = pd.read_json(df_info_data)
        df = df[['gene', 'product']]
        file_out = 'syndive_proteinInfo.csv'
    elif triggered_id == 'export-enrichment':
        df = pd.read_json(df_enriched_data)
        file_out = 'syndive_proteinEnriched.csv'
        PreventUpdate
    elif triggered_id == 'export-abundance':
        df = pd.read_json(df_expressed_data)
        file_out = 'syndive_proteinExpressed.csv'
        PreventUpdate
    else:
        PreventUpdate

    df = df.reset_index().rename(columns={'index':'protein'})
    return dict(content=df.to_csv(index=False, encoding='utf-8'), 
                 filename=file_out, type='text/csv')




## ---
## update plot cytoscape selected
## ---
@app.callback(
    Output('plot-cytoscape', 'elements'),
    Input('select-cytoscape-term', 'value'),
    prevent_initial_callbacks=False
)
def select_cyto_value(selected_id):
    updated_nodes = []
    for node in cyto_nodes:
        if node['data']['protein'] == selected_id:
            node['selected'] = True
        else:
            node['selected'] = False
        updated_nodes.append(node)
    return updated_nodes + cyto_edges


## ---
## update plot cytoscape colors
## ---
@app.callback(
    Output('plot-cytoscape', 'stylesheet'),
    Input('select-cytoscape-color', 'value')
)
def select_cyto_color(selected_color):
    background_color = 'data(color_vglut)'
    if selected_color == 'vglut':
        background_color = 'data(color_vglut)'
    elif selected_color == 'vgat':
        background_color = 'data(color_vgat)'
    elif selected_color == 'modules':
        background_color = 'data(color_module)'
    
    new_style_sheet = [
            {
                'selector': 'node',
                'style': {
                    'background-color': background_color,
                    'label': 'data(gene)'
                }
            }, {
                'selector': 'edge',
                'style': {
                    'width': 1,
                    'line-color': '#778899'
                }
            }, {
                'selector': ':selected',
                'style': {
                    'border-width': 10,
                    'border-color': '#2F4F4F',
                    'width':100,
                    'height':100,
                    'font-size': 100,
                    'z-index': 1
                }
        },
    ]

    return new_style_sheet



## ---
## update plot cytoscape info
## ---
@app.callback(
    Output('text-cytoscape', 'value'),
    Input('plot-cytoscape', 'selectedNodeData')
)
def update_node_info(selected_node_data):
    info_text = 'No node selected.'
    if selected_node_data:
        # selected_id = selected_node_data[0]['id']
        gene = f"gene: {selected_node_data[0]['gene']}\n"
        protein = f"protein: {selected_node_data[0]['protein']}\n"
        module = f"synaptic module: {selected_node_data[0]['module']}\n"
        vglut = f"corr.VGLUT: {selected_node_data[0]['vglut']:.3g}\n"
        vgat = f"corr.VGAT: {selected_node_data[0]['vgat']:.3g}\n"
        interactors = f"neighbours: {selected_node_data[0]['interactors']}\n"
        interactors_top = f"strongest correlates: {selected_node_data[0]['interactors_top']}\n"
        info_text = gene + protein + module + vglut + vgat + interactors + interactors_top
        
    return info_text 

if __name__ == '__main__':
    app.run(debug=True, port=8051)
