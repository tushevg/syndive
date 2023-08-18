import json
import pandas as pd
import matplotlib.colors as mcolors


# create linear gradient based on color values
def generate_correlation_color(value_corr, value_min=-1, value_max=1,
                               color_min = '#1E90FF', color_mid = 'white', color_max = '#FF4500'):

    colormap = mcolors.LinearSegmentedColormap.from_list(
        'correlation_cmap', [color_min, color_mid, color_max])
    normalized_value = (value_corr - value_min) / (value_max - value_min)
    color_hex = mcolors.to_hex(colormap(normalized_value))
    return color_hex

# update interactors based on current edge
def update_interactors(interactors: dict, edge: dict):
    interactors.setdefault(edge['source'], {})[edge['target']] = edge['freq']
    interactors.setdefault(edge['target'], {})[edge['source']] = edge['freq']


# read json network
with open('./prototypes/adjacency_list_03.csv.json', 'r') as f:
    elements = json.loads(f.read())

# read meta data
df_vglut = pd.read_csv('./prototypes/vGlut1_geneInfo.csv', sep = ',', index_col=1)
df_vgat = pd.read_csv('./prototypes/vGAT_geneInfo.csv', sep = ',', index_col=1)
df_modules = pd.read_csv('./prototypes/syndive_module_colors.csv', sep=',', index_col=0)

df_meta = pd.DataFrame({'gene': df_vglut['GeneName'],
                'protein': df_vglut.index,
                'module': df_vglut['Module'],
                'vGlut': df_vglut['GS.vGAT'],
                'vGat': df_vgat['GS.vGAT']})
df_meta.set_index('protein', inplace=True)
df_meta.loc['TdTomato', 'gene'] = 'TdTomato'

# filter coordinates
x_filter = 1300
y_filter = -1400

node_filter = []
node_map = {}
el = elements['elements']
cytograph = {'nodes':[], 'edges':[]}

# loop over nodes
for node in el['nodes']:

    x = node['position']['x']
    y = node['position']['y']

    if (x > x_filter) and (y < y_filter):
        node_filter.append(node['data']['id'])
        # print(x,y)
        continue

    protein = node['data']['Proteins']
    gene = df_meta.loc[protein, 'gene']
    module = df_meta.loc[protein, 'module']
    node_map[node['data']['id']] = gene
    cytonode = {
        'data':{
            'id': node['data']['id'],
            'protein': protein,
            'gene': gene,
            'module': module,
            'color_module': df_modules.loc[module,'color'],
            'vglut': node['data']['GS_vGlut1'],
            'color_vglut': generate_correlation_color(node['data']['GS_vGlut1']),
            'vgat': node['data']['GS_vGAT'],
            'color_vgat': generate_correlation_color(node['data']['GS_vGAT']),
            'interactors': 0,
            'interactors_top': ''
        },
        'position':{'x':x, 
                    'y':y},
        'selected': False,
        'selectable': True,
        'locked': False,
        'grabbable': True}
    cytograph['nodes'].append(cytonode)


# loop over edges
interactors = {}
for edge in el['edges']:
    
    if (edge['data']['source'] in node_filter) or (edge['data']['target'] in node_filter):
       continue

    cytoedge = {
        'data': {
            'id': edge['data']['id'],
            'source': edge['data']['source'],
            'target': edge['data']['target'],
            # 'source_gene': node_map[edge['data']['source']],
            # 'target_gene': node_map[edge['data']['target']],
            'freq': edge['data']['Freq']
        },
        'selected': False,
        'selectable': False
    }
    cytograph['edges'].append(cytoedge)
    tmp = cytoedge['data']
    update_interactors(interactors, cytoedge['data'])
    

n_top = 10
for node in cytograph['nodes']:
    id = node['data']['id']
    interplay = interactors[id]
    # Sort dictionary keys by values
    sorted_keys = sorted(interplay, key=interplay.get, reverse=True)
    sorted_genes = []
    n = 0
    for key in sorted_keys:
        sorted_genes.append(node_map[key])
        n = n + 1
        if n >= n_top:
            break

    node['data']['interactors'] = len(sorted_keys)
    node['data']['interactors_top'] = ', '.join(sorted_genes)


# write to file
json_object = json.dumps(cytograph, indent=4)
with open('cytoscape_info.json', "w") as json_file:
    json_file.write(json_object)
