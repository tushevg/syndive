import sqlite3
import pandas as pd
import dash
from dash import dcc, html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Connect to the SQLite database and create a sample table
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sample_table (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT
)
""")

# Sample data
data = [
    ('Alice', 25, 'New York'),
    ('Bob', 30, 'San Francisco'),
    ('Cathy', 27, 'Los Angeles'),
    ('David', 22, 'Chicago'),
    ('Eva', 29, 'Houston'),
    ('Frank', 34, 'Austin'),
    ('Grace', 24, 'Seattle'),
    ('Hank', 31, 'Miami'),
    ('Ivan', 28, 'Boston'),
    ('Jack', 26, 'Denver'),
    ('Karen', 33, 'Atlanta'),
    ('Liam', 32, 'Dallas')
]

cursor.executemany("""
INSERT OR IGNORE INTO sample_table (name, age, city)
VALUES (?, ?, ?)
""", data)

conn.commit()

offset = 0
limit = 10

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Dash App with SQLite3 Database'),
            html.Img(src='/assets/logo.png', height='60px')
        ], className='text-center py-3')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Input(id='search-input', type='text', placeholder='Search by name', className='w-100'),
            html.Button('Search', id='search-button', className='btn btn-primary w-100 mt-2'),
            html.Div(id='search-output', className='mt-2')
        ], width=4),
        dbc.Col([
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in ['id', 'name', 'age', 'city']],
                data=[],
                page_size=10,
                style_table={'overflowX': 'auto'}
            ),
            dbc.ButtonGroup([
                dbc.Button('Previous', id='previous-button', className='btn btn-secondary'),
                dbc.Button('Next', id='next-button', className='btn btn-secondary')
            ], className='d-flex justify-content-center mt-2'),
            html.Div(id='page-info', className='text-center mt-2')
        ], width=8)
    ])
], fluid=True)

@app.callback(
    Output('data-table', 'data'),
    Output('page-info', 'children'),
    Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks'),
    Input('search-button', 'n_clicks'),
    State('search-input', 'value'),
    prevent_initial_call=True
)
def update_table(prev_click, next_click, search_click, search_value):
    ctx = dash.callback_context
    global offset
    if not ctx.triggered:
        return [], ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'previous-button' and offset >= limit:
        offset -= limit
    elif button_id == 'next-button':
        offset += limit
    elif button_id == 'search-button':
        offset = 0
