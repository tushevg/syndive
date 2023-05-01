import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

searchbar = html.Div(dmc.TextInput(
    style={"width": 400},
    placeholder="Search a gene",
    icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal')),
    style={"display": "flex", "justifyContent": "center", "marginTop": "80px"})
