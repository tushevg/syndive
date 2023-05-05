import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from dash import dcc
import re

def plot_expressd(df_expressed, search_term):
    df = df_expressed.set_index('protein')
    record = df.loc[search_term]

    list_regions = []
    list_mouseline = []
    list_values = []
    for key, value in record.items():
        if value > 0:
            key = re.sub(r'\.\d+$', '', key)
            region, mouseline = str.split(key, sep='.')
            if mouseline != "Unsorted":
                mouseline = mouseline + "-cre"
            list_regions.append(region)
            list_mouseline.append(mouseline)
            list_values.append(value)
    df = pd.DataFrame({'values': list_values, 'regions': list_regions, 'mouse line': list_mouseline})


    list_unq_regions = ['Cerebellum', 'Cortex', 'Hippocampus', 'OlfactoryBulb', 'Striatum']
    list_unq_mouseline = ['Unsorted', 'Camk2a-cre', 'Dat1-cre', 'Syn1-cre', 'Gad2-cre', 'PV-cre', 'SST-cre', 'VIP-cre']
    color_map = {'Unsorted': '#708090', 
                'Camk2a-cre': '#1E90FF', 
                'Dat1-cre': '#00BFFF',
                'Syn1-cre': '#32CD32',
                'Gad2-cre': '#FF6347',
                'PV-cre': '#9400D3',
                'SST-cre': '#FFD700',
                'VIP-cre': '#FFA500'}

    fig = px.box(df, x='regions', y='values',
                 title='Synaptic Expression',
                color='mouse line',
                color_discrete_map=color_map,
                category_orders={'regions': list_unq_regions, 'mouse line': list_unq_mouseline},
                template='plotly_white')

    for vidx in range(len(list_unq_regions) - 1):
        fig.add_vline(x=vidx + .5, line_color='grey', line_width=0.5)

    fig.update_layout(xaxis_title='',
                    yaxis_title='protein expression')
    
    return fig