import dash_mantine_components as dmc
from dash import Dash

# Define the external stylesheet with the Google font
external_stylesheets = ['https://fonts.googleapis.com/css?family=Inter']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True
