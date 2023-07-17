from dash import Dash, dcc, html
from dash import callback, Output, Input, State, ctx, ALL, clientside_callback
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import pandas as pd
from fast_autocomplete import AutoComplete
import os

# Get the absolute path to the current file
#current_path = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the styles.css file
#styles_path = os.path.join(current_path, '../prototypes/styles.css')


app = Dash(__name__, prevent_initial_callbacks=True)


app.layout = html.Div(
    className="app-container",
    children=[
        html.Div(dmc.Text("PannelA"), className="section dark"),
        html.Div(dmc.Text("PannelB"), className="section light")
    ]
)

if __name__ == '__main__':
    app.run(debug=True)