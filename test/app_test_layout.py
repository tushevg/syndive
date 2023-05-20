from dash import Dash, dcc, html, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify


from layouts.header import header



app = Dash(__name__, 
           prevent_initial_callbacks=True,
           assets_folder='../assets',
           )

app.layout = html.Div([
    header(),
    dmc.Paper([dmc.Text("Synaptic Diversity Hub")]),
])

if __name__ == '__main__':
    app.run_server(debug=True)