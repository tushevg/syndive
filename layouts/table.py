import sqlite3
import pandas as pd
import dash_mantine_components as dmc
from dash import html


def read_rows_from_db_table(db_file, db_table, start_idx, num_rows):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    query = f"SELECT * FROM {db_table} LIMIT {num_rows} OFFSET {start_idx}"
    c.execute(query)
    results = c.fetchall()
    column_names = [description[0] for description in c.description]
    conn.close()
    df = pd.DataFrame(results, columns=column_names)
    return df


def create_table(df):
    def format_float(value, is_float):
        if is_float:
            return format(value, ".3f")
        return value

    # Define center-aligned style
    center_style = {'textAlign': 'center'}

    # Add style to the headers
    header = [html.Tr([html.Th(col, style=center_style) for col in df.columns])]

    rows = []
    for _, row in df.iterrows():
        # Add style to the cells
        formatted_row = [html.Td(format_float(value, dtype == 'float64'), style=center_style) for value, dtype in zip(row, df.dtypes)]
        rows.append(html.Tr(formatted_row))

    table = [html.Thead(header), html.Tbody(rows)]
    return table


db_file = 'data/rnaseq_cortex.db'
db_table = 'deseq'

df = read_rows_from_db_table(db_file, db_table, 100, 10)
table_html = create_table(df)

table = html.Div([
            html.Div([dmc.Table(verticalSpacing="sm",
                                horizontalSpacing=10,
                                children=table_html)],
                                style={"width": "80%"})],
        style={"display": "flex", "justifyContent": "center"})

