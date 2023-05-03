import sqlite3
import pandas as pd
from dash import html


def convert_sqlite3_dtypes(df, conn, db_table):
    cursor = conn.cursor()
    table_info = cursor.execute(f"PRAGMA table_info({db_table})").fetchall()

    dtype_map = {
        'INTEGER': 'int64',
        'REAL': 'float64',
        'TEXT': 'str',
        'BLOB': 'object',
        'NUMERIC': 'object',
    }

    for _, column_name, data_type, _, _, _ in table_info:
        if data_type in dtype_map:
            df[column_name] = df[column_name].astype(dtype_map[data_type])

    return df



def read_rows_from_db_table(db_file, db_table, start_idx, num_rows):
    conn = sqlite3.connect(db_file)
    query = f"SELECT * FROM {db_table} LIMIT {num_rows} OFFSET {start_idx}"
    df = pd.read_sql_query(query, conn)
    df = convert_sqlite3_dtypes(df, conn, db_table)
    conn.close()
    return df


def create_table(df):
    def format_float(value, is_float):
        if is_float:
            return format(value, ".3f")
        return value

    header = [html.Tr([html.Th(col) for col in df.columns])]
    
    rows = []
    for _, row in df.iterrows():
        formatted_row = [html.Td(format_float(value, dtype == 'float64')) for value, dtype in zip(row, df.dtypes)]
        rows.append(html.Tr(formatted_row))
    
    table = [html.Thead(header), html.Tbody(rows)]
    return table

db_file = 'data/rnaseq_cortex.db'
db_table = 'deseq'

df = read_rows_from_db_table(db_file, db_table, 100, 10)
print(df.dtypes)