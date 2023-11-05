import os
from dash import Dash, dcc, html, callback, Output, Input, State, ctx, ALL, clientside_callback
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from layouts2.header import header
from layouts2.body import body
from layouts2.footer import footer

from dash_intersection_observer import DashIntersectionObserver

url_custom_path = os.getenv('SYNDIVE_URLPATH', '')
if not url_custom_path.endswith('/'):
    url_custom_path = url_custom_path + '/'


app = Dash(__name__, 
           external_stylesheets=['https://fonts.googleapis.com/css2?family=Roboto'], 
           prevent_initial_callbacks=True,
           requests_pathname_prefix=url_custom_path)
server = app.server
app.title = 'syndive'

app.layout = dmc.Container(id='id-layout', fluid=True,
                           children=[
                               header(),
                               body(),
                               footer()])

@app.callback(
    Output('id-searchbar-header', 'style'),
    Input('id-observer', 'inView')
)
def handle_observer(in_view):
    if in_view:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


if __name__ == '__main__':
    app.run(debug=True, port=8058)