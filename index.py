import os
from dash import dcc
from dash import html
import dash_mantine_components as dmc

from app import app
from layouts.header import header
from layouts.searchbar import searchbar
from layouts.footer import footer
from layouts.table import table

# https://www.fontspace.com/futuristic-font-f41324

app.layout = html.Div([
    header,
    searchbar,
    table,
    html.Hr(style={"border": "0.1px solid #ccc"}),
    footer
])

if __name__ == '__main__':
    app.run_server(debug = True)

