import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from dash import dcc

# define common plots variables
label_region = ['Cortex', 
                'Cortical IN', 
                'Hippocampus', 
                'Striatum', 
                'Cerebellum', 
                'Olfactory Bulb']

label_mouseline = ['Camk2a-cre', 
                    'Dat1-cre', 
                    'Syn1-cre', 
                    'Gad2-cre', 
                    'PV-cre', 
                    'SST-cre', 
                    'VIP-cre']

# color_map match paper
color_map = {'Unsorted': '#708090',
            'Not enriched': '#DCDCDC',
            'Camk2a-cre': '#C3BE04', 
            'Dat1-cre': '#409E36',
            'Syn1-cre': '#AAD4AC',
            'Gad2-cre': '#E94879',
            'PV-cre': '#D15196',
            'SST-cre': '#F3A1AE',
            'VIP-cre': '#B77CA3'}

# color_map web page
# color_map = {'Unsorted': '#708090',
#             'Not enriched': '#DCDCDC',
#             'Camk2a-cre': '#1E90FF', 
#             'Dat1-cre': '#00BFFF',
#             'Syn1-cre': '#32CD32',
#             'Gad2-cre': '#FF6347',
#             'PV-cre': '#9400D3',
#             'SST-cre': '#FFD700',
#             'VIP-cre': '#FFA500'}



# dot-plot data frame
def get_dotplot_df(df_info: pd.DataFrame, df_enriched: pd.DataFrame) -> pd.DataFrame:
    y = -1
    val_x = []
    val_y = []
    val_gene = []
    val_protein = []
    val_region = []
    val_mouseline = []
    val_xoffset = [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3]
    for protein, row in df_info.iterrows():
        gene = row[0]
        y = y + 1
        nonenriched_region = label_region.copy()
        # check if enriched
        if protein in df_enriched.index:
            row_enriched = df_enriched.loc[protein]
            for label_column, value in row_enriched.items():
                if value == 1:
                    region, mouseline = str.split(label_column, sep='.')
                    x = label_region.index(region)
                    x_offset = label_mouseline.index(mouseline)
                    val_x.append(val_xoffset[x_offset] + x + 1)
                    val_y.append(y)
                    val_gene.append(gene)
                    val_protein.append(protein)
                    val_region.append(region)
                    val_mouseline.append(mouseline)
                    
                    if region in nonenriched_region:
                        nonenriched_region.remove(region)
        
        if nonenriched_region:
            x = [index + 1 for index, value in enumerate(label_region) if value in nonenriched_region]
            val_x.extend(x)
            val_y.extend([y] * len(nonenriched_region))
            val_gene.extend([gene] * len(nonenriched_region))
            val_protein.extend([protein] * len(nonenriched_region))
            val_region.extend(nonenriched_region)
            val_mouseline.extend(['Not enriched'] * len(nonenriched_region))
 

    df_dotplot = pd.DataFrame({'x': val_x, 'y': val_y, 
                            'region': val_region,
                            'mouse line': val_mouseline,
                            'gene': val_gene,
                            'protein': val_protein})
    
    return df_dotplot




# dot-plot figure
def plot_dotplot(df_info: pd.DataFrame,
                 df_enriched: pd.DataFrame,
                 label_yaxis: str = 'gene',
                 label_title: str = 'Synapse-Type Enrichment') -> px.scatter:
    labels = df_info['gene'].to_list()
    df_dotplot = get_dotplot_df(df_info=df_info, df_enriched=df_enriched)
    fig = px.scatter(df_dotplot, x='x', y='y', color='mouse line', opacity=0.8,
                    category_orders={'regions': label_region, 'mouse line': label_mouseline},
                    color_discrete_map=color_map,
                    template='plotly_white',
                    hover_name = 'gene',
                    hover_data={'region':True,'x':False,'mouse line':True, 'protein':True, 'gene':False, 'y':False})

    fig.update_layout(xaxis=dict(tickmode="array", 
                                tickvals=list(range(1, len(label_region) + 1)),
                                ticktext=label_region),
                    yaxis=dict(tickmode="array",
                                tickvals=list(range(0, len(labels) + 1)),
                                ticktext=labels),
                    xaxis_range=[0.3, len(label_region) + 0.7],
                    yaxis_range=[-0.5, len(labels) - 0.5],
                    xaxis_title='',
                    yaxis_title=label_yaxis,
                    title=label_title
                    )

    for vidx in range(len(label_region)+1):
            fig.add_vline(x=vidx + .5, line_color='grey', line_width=0.5)

    return fig




# box-plot data frame
def get_boxplot_df(df: pd.DataFrame, key: str) -> pd.DataFrame:
    if key not in df.index:
        default_value = [0] * len(label_region) * len(label_mouseline)
        default_regions = [item for item in label_region for _ in range(len(label_mouseline))]
        default_mouseline = label_mouseline * len(label_region)
        return pd.DataFrame({'values': default_value,
                             'regions': default_regions,
                             'cell type': default_mouseline})
    record = df.loc[key]
    list_regions = []
    list_celltypes = []
    list_values = []
    for key, value in record.items():
        if value != 0.0:
            region, celltype, _ = str.split(key, sep='.')
            list_regions.append(region)
            list_celltypes.append(celltype)
            list_values.append(value)
    df_boxplot = pd.DataFrame({'values': list_values, 'regions': list_regions, 'cell type': list_celltypes})
    return df_boxplot

# box-plot figure
def plot_boxplot(df: pd.DataFrame, key: str,
                 label_yaxis: str = 'protein abundance',
                 label_title: str = 'Synaptic Abundance') -> px.box:
    df_boxplot = get_boxplot_df(df = df, key = key)
    fig = px.box(df_boxplot, x='regions', y='values', 
                color='cell type',
                color_discrete_map=color_map,
                title= label_title,
                category_orders={'regions': label_region, 'mouse line': label_mouseline},
                template='plotly_white')

    for vidx in range(len(label_region) - 1):
        fig.add_vline(x=vidx + .5, line_color='grey', line_width=0.5)

    fig.update_layout(xaxis_title='',
                    yaxis_title=label_yaxis)
    fig.update_xaxes(range=[-0.5, len(label_region) - 0.5])
    
    return fig



def paper_dotplot(df_info, df_expressed):
    return dmc.Paper(dcc.Graph(id='plot-enriched', 
                               figure=plot_dotplot(df_info, df_expressed)),
                    shadow="sm", withBorder=True, p='sm', style={'width':'80%', 'margin':'2%'})



def update_select_data(df_info):
    data = []
    for value, row in df_info.iterrows():
        label = row['gene']
        item = {'value': value, 'label': label}
        data.append(item)
    return data



def paper_boxplot(df_info, df_expressed):
    data = update_select_data(df_info)
    select_term = data[0]['value']

    return dmc.Paper(dmc.Stack([
        dmc.Center(dmc.Select(data=data, id='select-term', value=select_term)),
        dcc.Graph(id='plot-expressed', figure=plot_boxplot(df_expressed, select_term)),
        dmc.Center(
            dmc.RadioGroup([dmc.Radio('abundance', value='abundance'),
                                    dmc.Radio('fold change (compare between regions)', value='fold-change')],
                    id='select-abundance',
                    value='abundance',
                    size='sm',
                    spacing='xl',
                    mt=10)
        )
    ]), shadow='sm', withBorder=True, p='sm', style={'width':'80%', 'margin': '2%'})
