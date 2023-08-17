from dash import Dash, dcc, html, callback, Output, Input, State, ctx, ALL
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_cytoscape as cyto
from dash import html
import json

import os
import sys

sys.path.append('/Users/tushevg/Desktop/syndive')
import layouts.dbtools as db
from layouts.plots import paper_cytoscape


def path_is_in_pythonpath(path):
    path = os.path.normcase(path)
    return any(os.path.normcase(sp) == path for sp in sys.path)

path_project = os.path.dirname(os.path.abspath(os.getcwd()))
if not path_is_in_pythonpath(path_project):
    sys.path.append(path_project)

# read cytoscape data
with open('../data/cytoscape_info.json', 'r') as f:
    elements = json.loads(f.read())
cyto_nodes = elements['nodes']
cyto_edges = elements['edges']

# read database
db_file = '../data/mpibr_synprot.db'
query_list = ['Gad1', 'Gad2', 'Slc32a1', 'Slc17a7',
               'Shank1', 'Syt2', 'Th']
df_info = db.listToDataFrame(search_list=query_list, db_column='gene',
                             db_table='info', db_file=db_file)





app = Dash(__name__)
server = app.server
app.title = 'syndive'

app.layout = html.Div([
    paper_cytoscape(cyto_nodes, cyto_edges, df_info)
])



## ---
## update plot expressed figure
## ---
@app.callback(
    Output('plot-cytoscape', 'elements'),
    Input('select-cytoscape-term', 'value')
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


# Callback to update multiple properties on the stylesheet
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


@app.callback(
    Output('text-cytoscape', 'value'),
    Input('plot-cytoscape', 'selectedNodeData')
)
def update_node_info(selected_node_data):
    info_text = 'No node selected.'
    if selected_node_data:
        selected_id = selected_node_data[0]['id']
        gene = selected_node_data[0]['gene']
        protein = selected_node_data[0]['protein']
        module = selected_node_data[0]['module']
        vglut = selected_node_data[0]['vglut']
        vgat = selected_node_data[0]['vgat']
        
        interactors = []
        interactors_count = 0
        for edge in cyto_edges:
            if edge['data']['source'] == selected_id:
                interactors.append({'gene': edge['data']['target_gene'], 'freq': edge['data']['freq']})
                interactors_count = interactors_count + 1
            if edge['data']['target'] == selected_id:
                interactors.append({'gene': edge['data']['source_gene'], 'freq': edge['data']['freq']})
                interactors_count = interactors_count + 1

        sorted_interactors = sorted(interactors, key=lambda x: x['freq'], reverse=True)
        top_ids = [interactor['gene'] for interactor in sorted_interactors]
        top_10_ids = top_ids[:10]

        info_text = f"gene: {gene}\nprotein: {protein}\nsynaptic module: {module}\ncorr.VGLUT: {vglut:.3g}\ncorr.VGAT: {vgat:.3g}\ninteractors: {interactors_count}\ntop genes: {', '.join(top_10_ids)}"
        
    return info_text


# # Callback to update selected node data when a node is tapped
# @app.callback(
#     Output('plot-cytoscape', 'selectedNodeData'),
#     Input('plot-cytoscape', 'tapNode')
# )
# def update_selected_node_data(tap_node):
#     if tap_node:
#         return [tap_node['data']]
#     return []



if __name__ == '__main__':
    app.run_server(debug=True)