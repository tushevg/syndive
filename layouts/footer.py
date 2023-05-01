import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

logo_mpibrain = dmc.Image(src='../assets/logo_mpibrain.png', width=100)
logo_scic = dmc.Image(src='../assets/logo_scic.png', width=100)

footer = dmc.Header(
    height=60,
    position='bottom',
    withBorder=True,
    style={"display": "flex", "align-items": "center",
    "justify-content": "space-between", "padding": "16px"},
    children=[
        logo_mpibrain,
        html.Div([
        dmc.Text("created with  ", size='xs', color='#2F4F4F'),
        DashIconify(icon='mdi:cards-heart-outline', color='red', width=24, height=24),
        dmc.Text("  by scic with dash", size='xs', color='#2F4F4F'),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "center"}),
        logo_scic])
