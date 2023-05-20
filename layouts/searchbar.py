import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

def searchbar():
    return dmc.Select(id='search-term', 
                    placeholder='Search gene or protein',
                    data=[],
                    searchable=True,
                    limit=20,
                    clearable=True,
                    icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal'),
                    style={"width": 400})