import dash
import dash_mantine_components as dmc
from dash import dcc, html, callback, Output, Input, State
from dash_iconify import DashIconify
import sqlite3


searchbar = html.Div([
    dcc.Input(id='search-bar',
              type='text',
              placeholder='Enter your search query ...',
              debounce=True),
    html.Div(id='search_output')
],
style={"display": "flex", "justifyContent": "center", "marginTop": "80px"})

# searchbar = html.Div([
#     dmc.TextInput(
#     label='',
#     value='',
#     id='search-bar',
#     type='search',
#     style={"width": 400, 'margin': '0% 1%'},
#     placeholder="Search gene or protein",
#     icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal')),
#     dmc.Button('Test', id='button_test'),
#     dmc.Text(id='test_output')],
#     style={"display": "flex", "justifyContent": "center", "marginTop": "80px"})

# Define the callback function that will handle search bar input
@callback(
    Output('search_output', 'children'),
    [Input('search_bar', 'n_submit')],
    [State('search_bar', 'value')]
)
def update_output(n_submit, search_value):
    if n_submit:
        return f'Search query: {search_value}'
    else:
        return 'Please press Enter to search.'

    # if n_submit and search_term:
    #     # Perform search here and return the results as a list
    #     search_results = [f'Result {i}' for i in range(1, 6) if str(i) in search_term]
    #     if search_results:
    #         return html.Ul([html.Li(result) for result in search_results])
    #     else:
    #         return html.P('No results found.')
    # else:
    #     return ''



