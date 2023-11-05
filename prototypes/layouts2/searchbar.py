import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

def searchbar(id, style, w):
    return dmc.Select(
        id=id,
        style=style,
        placeholder='Search gene or protein ...',
        data=[],
        maw=w,
        searchable=True,
        limit=20,
        clearable=True,
        icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal')
    )