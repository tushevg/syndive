import dash_mantine_components as dmc
from dash import html

def plot_cytoscape():
    return dmc.Stack([dmc.Text("Synaptic Pathways"),
        dmc.Image(src='assets/cytoscape.png')],
        style={"marginLeft": 40, "marginRight": 40, "marginTop": 40,"marginBottom": 40})