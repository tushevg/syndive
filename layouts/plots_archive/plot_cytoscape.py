import dash_mantine_components as dmc
from dash import html

def plot_cytoscape():
    return dmc.Paper(dmc.Stack([dmc.Text("Synaptic Pathways"),
        dmc.Image(src='assets/cytoscape.png')]), 
        shadow='sm', withBorder=True, p='sm', style={'width':'80%', 'margin': '2%'})




