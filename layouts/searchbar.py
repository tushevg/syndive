import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

def searchbar():
    return dmc.TextInput(id='search-term', 
                    placeholder='Search gene or protein',
                    type='search',
                    icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal'))