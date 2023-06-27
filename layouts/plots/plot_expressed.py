import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from dash import dcc
import re

def plot_expressed(df_expressed, search_term):
    record = df_expressed.loc[search_term]
    list_regions = []
    list_celltypes = []
    list_values = []
    for key, value in record.items():
        if value > 0.0:
            key = re.sub(r'\.\d+$', '', key)
            region, celltype = str.split(key, sep='.')
            region = region.replace('CorticalInterneurons', 'Cortical IN')
            list_regions.append(region)
            list_celltypes.append(celltype)
            list_values.append(value)
    df = pd.DataFrame({'values': list_values, 'regions': list_regions, 'cell type': list_celltypes})


    list_unq_region = ['Cortex', 'Cortical IN', 'Hippocampus', 'Striatum', 'Cerebellum', 'OlfactoryBulb']
    list_unq_mouse = ['Camk2a-cre', 'Dat1-cre', 'Syn1-cre', 'Gad2-cre', 'PV-cre', 'SST-cre', 'VIP-cre']

    color_map = {'Unsorted': '#708090', 
                'Camk2a-cre': '#1E90FF', 
                'Dat1-cre': '#00BFFF',
                'Syn1-cre': '#32CD32',
                'Gad2-cre': '#FF6347',
                'PV-cre': '#9400D3',
                'SST-cre': '#FFD700',
                'VIP-cre': '#FFA500'}

    fig = px.box(df, x='regions', y='values', 
                color='cell type',
                color_discrete_map=color_map,
                title='Abundance',
                category_orders={'regions': list_unq_region, 'mouse line': list_unq_mouse},
                template='plotly_white')

    for vidx in range(len(list_unq_region) - 1):
        fig.add_vline(x=vidx + .5, line_color='grey', line_width=0.5)

    fig.update_layout(xaxis_title='',
                    yaxis_title='protein abundance')
    
    return fig


def paper_expressed(df_info, df_expressed):
    data = update_select_data(df_info)
    select_term = data[0]['value']
    return dmc.Paper(dmc.Stack([
        dmc.Center(dmc.Select(data=data, id='select-term', value=select_term)),
        dcc.Graph(id='plot-expressed', figure=plot_expressed(df_expressed, select_term))
    ]), shadow='sm', withBorder=True, p='sm', style={'width':'80%', 'margin': '2%'})


def update_select_data(df_info):
    data = []
    for value, row in df_info.iterrows():
        label = row['gene']
        item = {'value': value, 'label': label}
        data.append(item)
    return data