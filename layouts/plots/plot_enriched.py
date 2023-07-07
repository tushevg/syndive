import numpy as np
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from dash import dcc

def plot_enriched(df_info, df_enriched):
    list_brain = []
    list_mouse = []
    for key in df_enriched.columns:
        brain, mouse = str.split(key, sep='.')
        list_brain.append(brain)
        list_mouse.append(mouse)

    list_unq_brain = ['Cortex', 'CorticalInterneurons', 'Hippocampus', 'Striatum', 'Cerebellum', 'OlfactoryBulb']
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
    for protein, row_info in df_info.iterrows():
        label_y.append(row_info['gene'])
        row_enriched = df_enriched.loc[protein]
        for key, value in row_enriched.items():
            if value == 1:
                brain, mouse = str.split(key, sep='.')
                value_x_shift = list_unq_mouse.index(mouse)
                value_x_tick = list_unq_brain.index(brain) + 1
                value_x_point = value_x_tick + (value_x_min + value_x_step * value_x_shift)
                value_x.append(value_x_point)
                value_y.append(len(label_y) - 1)
                label_mouse.append(mouse)
                label_gene.append(row_info['gene'])
                label_brain.append(brain)

    df = pd.DataFrame({'x': value_x, 'y': value_y, 'mouse line': label_mouse, 'gene': label_gene, 'region': label_brain})

    color_map = {'Camk2a-cre': '#1E90FF', 
                'Dat1-cre': '#00BFFF',
                'Syn1-cre': '#32CD32',
                'Gad2-cre': '#FF6347',
                'PV-cre': '#9400D3',
                'SST-cre': '#FFD700',
                'VIP-cre': '#FFA500'}

    label_x[1] = 'Cortical IN'
    
    fig = px.scatter(df, x='x', y='y', color='mouse line', opacity=0.8,
                    title='Synapse-Type Enrichment',
                    category_orders={'mouse line': list_unq_mouse},
                    color_discrete_map=color_map,
                    template='plotly_white',
                    hover_name = 'gene',
                    hover_data={'region':True,'x':False,'mouse line':True, 'gene':True, 'y':False})

    fig.update_layout(xaxis=dict(tickmode="array", tickvals=np.arange(0, len(label_x)) + 1,
                                ticktext=label_x),
                    yaxis=dict(tickmode="array", tickvals=np.arange(0, len(label_y)),
                                ticktext=label_y),
                    xaxis_range=[0.3, 6.7],
                    yaxis_range=[-0.5, len(label_y) - 0.5],
                    xaxis_title='',
                    yaxis_title='gene'
                    )
    
    #fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    for vidx in range(len(label_x)+1):
        fig.add_vline(x=vidx + .5, line_color='grey', line_width=0.5)
        
    return fig


def paper_enriched(df_info, df_expressed):
    return dmc.Paper(dcc.Graph(id='plot-enriched', figure=plot_enriched(df_info, df_expressed)),
                    shadow="sm", withBorder=True, p='sm', style={'width':'80%', 'margin':'2%'})