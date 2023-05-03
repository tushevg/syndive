from dash import Dash, dcc, html, callback, Output, Input, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px

from layouts.header import header
from layouts.footer import footer

app = Dash(__name__)

### --- HELPER FUNCTIONS --- ###

# database query by list
def dbquery_find_list(search_list: list,
                      db_row: str,
                      db_table: str,
                      db_file: str) -> pd.DataFrame:
    query = f"SELECT * FROM {db_table} WHERE {db_row} IN ({','.join(['?']*len(search_list))})"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=search_list)
    conn.close()
    return df


# database query by term
def dbquery_find_term(search_term: str,
                      db_table: str,
                      db_file: str) -> pd.DataFrame:
    query = f"SELECT * FROM {db_table} WHERE protein = ? OR gene = ?"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=[search_term, search_term])
    conn.close()
    return df


# create html table
def create_table_info(df):
    center_style = {'textAlign': 'center'}
    #header = [html.Tr([html.Th(col, style=center_style) for col in df.columns])]
    header = [html.Tr([html.Th('protein', style=center_style),
                       html.Th('gene', style=center_style)])]

    rows = []
    for _, row in df.iterrows():
        # Add style to the cells
        protein = row['protein']
        protein = html.Td(dmc.Anchor(protein, href=f"https://www.uniprot.org/uniprotkb/{protein}/entry"), style=center_style)
        gene = html.Td(dmc.HoverCard(
                    withArrow=True,
                    width=200,
                    shadow="md",
                    closeDelay="100ms",
                    children=[
                        dmc.HoverCardTarget(dmc.Text(row['gene'])),
                        dmc.HoverCardDropdown(dmc.Text(row['name'],size="sm"))],
                        style=center_style))
        formatted_row = [protein, gene]
        rows.append(html.Tr(formatted_row))

    table = [html.Thead(header), html.Tbody(rows)]
    return table


# create enrichment figure
def plot_enrichment(df_info, df_enriched):
    df = df_enriched.set_index('protein')
    list_brain = []
    list_mouse = []
    for key in df.columns:
        brain, mouse = str.split(key, sep='.')
        list_brain.append(brain)
        list_mouse.append(mouse)
    list_unq_brain = sorted(set(list_brain))
    list_unq_mouse = sorted(set(list_mouse))

    value_x_step = 0.125
    value_x_min = -0.25

    label_x = []
    label_y = list_unq_mouse
    label_gene = []
    label_region = []
    value_x = []
    value_y = []
    for value_x_tick, row_info in df_info.iterrows():
        label_x.append(row_info['gene'])
        row_enriched = df.loc[row_info['protein']]
        for key, value in row_enriched.items():
            if value == 1:
                brain, mouse = str.split(key, sep='.')
                value_x_shift = list_unq_brain.index(brain)
                value_x_point = (value_x_tick + 1) + (value_x_min + value_x_step * value_x_shift)
                value_x.append(value_x_point)
                value_y.append(list_unq_mouse.index(mouse) + 1)
                label_region.append(brain)
                label_gene.append(row_info['gene'])

    df = pd.DataFrame({'x': value_x, 'mouse': value_y, 'region': label_region, 'gene': label_gene})

    label_y[label_y.index('Camk2a')] = 'CAMK2A'
    label_y[label_y.index('Syn1')] = 'SYN1'
    label_y[label_y.index('Gad2')] = 'GAD2'
    label_y[label_y.index('Dat1')] = 'DAT'

    fig = px.scatter(df, x='x', y='mouse', color='region', opacity=0.8,
                    title='Synaptic Enrichment',
                    category_orders={'region': list_unq_brain},
                    template='plotly_white',
                    hover_name = 'gene',
                    hover_data={'region':True,'x':False,'mouse':True})
    #fig.update_traces(marker=dict(size=8))
    fig.update_layout(xaxis=dict(tickmode="array", tickvals=np.arange(0, len(label_x)) + 1,
                                ticktext=label_x),
                    yaxis=dict(tickmode="array", tickvals=np.arange(0, len(label_y)) + 1,
                                ticktext=label_y),
                    xaxis_title='gene',
                    yaxis_title='mouse',
                    )
    return fig


### --- ALLOCATE DATA --- ###
db_file = 'data/mpibr_synprot.db'
query_list = ['Gad1', 'Gad2', 'Dlg4', 
               'Shank1', 'Slc17a7', 'Slc32a', 
               'Slc6a3', 'Th']
df_info = dbquery_find_list(query_list, 'gene', 'info', db_file)
df_enriched = dbquery_find_list(df_info['protein'].to_list(), 'protein', 'enriched', db_file)
df_expressed = dbquery_find_list(df_info['protein'].to_list(), 'protein', 'expressed', db_file)


### -- CREATE ELMENTS PROTOTYPES --- ###
table_info = create_table_info(df_info)
fig_enriched = plot_enrichment(df_info, df_enriched)

### --- LAYOUT --- ###
app.layout = html.Div([
    dcc.Store(id='df-info', data=df_info.to_json()),
    dcc.Store(id='df-enriched', data=df_enriched.to_json()),
    dcc.Store(id='df-expressed', data=df_expressed.to_json()),
    header,
    dmc.Container(dmc.TextInput(id='search-term', 
                    placeholder='Search gene or protein',
                    type='search',
                    icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal')),
                    style={"width": "40%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"},
                    fluid=True),
    dmc.Container([
        dmc.Grid([dmc.Col(dmc.Table(id='table-output',
                    verticalSpacing="sm",
                    horizontalSpacing="sm",
                    highlightOnHover=True,
                    children=table_info), span=2),
                  dmc.Col(dcc.Graph(id='scatter-plot', figure=fig_enriched), span=8)],
                  gutter="xl",
                  grow=True)
    ],
                  style={"width": "90%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"},
                  fluid=True),
    footer
])


### --- CALLBACKS --- ###

# define a callback to update the dataframe        
@callback(
    [Output('df-info', 'data'),
     Output('table-output', 'children')],
    Input('search-term', 'n_submit'), # trigger
    State('df-info', 'data'),
    State('search-term', 'value'),
    prevent_initial_call=True
)
def search_data(n_submit, data, search_term):
    df = pd.read_json(data)
    df_query = df[(df['protein'] == search_term) | 
                  (df['gene'] == search_term)]
    if df_query.empty:
        df_query = dbquery_find_term(search_term, 'info', db_file)
        if not df_query.empty:
            df = pd.concat([df, df_query], ignore_index=True)
    table_html = create_table_info(df)
    return df.to_json(), table_html


if __name__ == '__main__':
    app.run_server(debug=True)
