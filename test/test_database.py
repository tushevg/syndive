import sqlite3
import pandas as pd

def dbquery_read_rows(db_file: str, 
                    db_table: str, 
                    sort_column: str,
                    start_idx: int = 0, 
                    num_rows: int = 10,
                    sort_order: str = 'ASC') -> pd.DataFrame:
    if sort_order.upper() not in ['ASC', 'DESC']:
        raise ValueError('sort_order must be "ASC" or "DESC"')
    query = f"SELECT * FROM {db_table} ORDER BY {sort_column} {sort_order} LIMIT {num_rows} OFFSET {start_idx}"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def dbquery_match_term(search_term: str,
                        db_table: str,
                        db_file: str) -> pd.DataFrame:
    query = f"SELECT * FROM {db_table} WHERE protein = ? OR gene = ?"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=[search_term, search_term])
    conn.close()
    return df


def dbquery_find_term(search_term: str,
                      db_table: str,
                      db_file: str) -> pd.DataFrame:
    query = f"SELECT * FROM {db_table} WHERE protein = ?"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=[search_term])
    conn.close()
    return df


def dbquery_get_terms(search_list: list,
                      db_table: str,
                      db_file: str) -> pd.DataFrame:
    query = f"SELECT * FROM {db_table} WHERE gene IN ({','.join(['?']*len(search_list))})"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=search_list)
    conn.close()
    return df


db_file = 'data/mpibr_synprot.db'

table_info = dbquery_read_rows(db_file, 'info', 'gene', 1000, 5)
print(table_info)

keys=['Camk2a','Actbl2','Dlg4']
table_test = dbquery_get_terms(keys, 'info', db_file)
print(table_test)


# qry_info = dbquery_match_term('Camk2a', 'info', db_file)
# print(qry_info)

# qry_enriched = dbquery_find_term(qry_info.loc[0, 'protein'], 'enriched', db_file)
# print(qry_enriched)

# qry_expressed = dbquery_find_term(qry_info.loc[0, 'protein'], 'expressed', db_file)
# print(qry_expressed)
