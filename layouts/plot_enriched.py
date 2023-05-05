import numpy as np
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from dash import dcc

def plot_enriched(df_info, df_enriched):
    df = df_enriched.set_index('protein')

    list_brain = []
    list_mouse = []
    for key in df.columns:
        brain, mouse = str.split(key, sep='.')
        if mouse != "Unsorted":
            mouse = mouse + "-cre"
        list_brain.append(brain)
        list_mouse.append(mouse)
    #list_unq_brain = sorted(set(list_brain))
    #list_unq_mouse = sorted(set(list_mouse), reverse=True)
    list_unq_brain = ['Cerebellum', 'Cortex', 'Hippocampus', 'OlfactoryBulb', 'Striatum']
    list_unq_mouse = ['Camk2a-cre', 'Dat1-cre', 'Syn1-cre', 'Gad2-cre', 'PV-cre', 'SST-cre', 'VIP-cre']

    value_x_step = 0.1
    value_x_min = -0.3

    label_x = list_unq_brain
    label_y = []
    label_gene = []
    label_mouse = []
    label_brain = []
    value_x = []
    value_y = []
    for value_y_tick, row_info in df_info.iterrows():
        label_y.append(row_info['gene'])
        row_enriched = df.loc[row_info['protein']]
        for key, value in row_enriched.items():
            if value == 1:
                brain, mouse = str.split(key, sep='.')
                if mouse != "Unsorted":
                    mouse = mouse + "-cre"
                value_x_shift = list_unq_mouse.index(mouse)
                value_x_tick = list_unq_brain.index(brain) + 1
                value_x_point = value_x_tick + (value_x_min + value_x_step * value_x_shift)
                value_x.append(value_x_point)
                value_y.append(value_y_tick)
                label_mouse.append(mouse)
                label_gene.append(row_info['gene'])
                label_brain.append(brain)

    df = pd.DataFrame({'x': value_x, 'gene': value_y, 'mouse line': label_mouse, 'gene': label_gene, 'region': label_brain})

    color_map = {'Camk2a-cre': '#1E90FF', 
                'Dat1-cre': '#00BFFF',
                'Syn1-cre': '#32CD32',
                'Gad2-cre': '#FF6347',
                'PV-cre': '#9400D3',
                'SST-cre': '#FFD700',
                'VIP-cre': '#FFA500'}

    fig = px.scatter(df, x='x', y='gene', color='mouse line', opacity=0.8,
                    title='Synaptic Enrichment',
                    category_orders={'mouse line': list_unq_mouse},
                    color_discrete_map=color_map,
                    template='plotly_white',
                    hover_name = 'gene',
                    hover_data={'region':True,'x':False,'mouse line':True, 'gene':False})

#yaxis=dict(tickmode="array", tickvals=np.arange(0, len(label_y)),
#                                ticktext=label_y),

    fig.update_layout(xaxis=dict(tickmode="array", tickvals=np.arange(0, len(label_x)) + 1,
                                ticktext=label_x),          
                    xaxis_range=[0.3, 5.7],
                    yaxis_range=[-0.5, len(label_y) - 0.5],
                    xaxis_title='',
                    yaxis_title='gene',
                    )

    for vidx in range(len(label_x)+1):
        fig.add_vline(x=vidx + .5, line_color='grey', line_width=0.5)
        
    return fig
