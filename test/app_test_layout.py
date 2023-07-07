from dash import Dash, dcc, html
from dash import callback, Output, Input, State, ctx, ALL, clientside_callback
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import pandas as pd
from fast_autocomplete import AutoComplete
import os

import sys
sys.path.append('/Users/tushevg/Desktop/syndive')


app = Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div(children = [
    dcc.Location(id='url', refresh=False),
    html.Div('no-size', id='print-size')
    ])


app.clientside_callback(
    """
       function(href) {
            function updateSize() {
                var w = window.innerWidth;
                return w;
            }
      
            // Update size on initial page load
            if (href === window.location.href) {
                return updateSize();
            }

            // Update size on browser window resize
            window.addEventListener('resize', function() {
                var size = updateSize();
                document.getElementById('print-size').innerText = size;
            });
        }
    """,
    Output('print-size', 'children'),
    Input('url', 'href')
)


if __name__ == '__main__':
    app.run(debug=True)