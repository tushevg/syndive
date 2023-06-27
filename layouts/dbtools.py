import sqlite3
import pandas as pd
from fast_autocomplete import AutoComplete


# read complete sqlite3 table to pandas data frame
def tableToDataFrame(db_table: str, db_file: str) -> pd.DataFrame:

    query = f'SELECT * FROM {db_table}'
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()
    df.set_index(df.columns[0], inplace=True)

    return df


# read list from sqlite database given key column
def listToDataFrame(search_list: list,
                    db_column: str,
                    db_table: str,
                    db_file: str) -> pd.DataFrame:
    
    query = f"SELECT * FROM {db_table} WHERE {db_column} IN ({','.join(['?']*len(search_list))})"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=search_list)
    conn.close()
    df.set_index(df.columns[0], inplace=True)

    return df


# read term from sqlite database given key column
def termToDataFrame(search_term: str,
                    db_column: str,
                    db_table: str,
                    db_file: str) -> pd.DataFrame:
    
    query = f"SELECT * FROM {db_table} WHERE {db_column} = ?"
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, conn, params=[search_term])
    conn.close()
    df.set_index(df.columns[0], inplace=True)

    return df


# set given count value to info table
def updateInfoCount(key: str,
                 db_column: str, db_key_column: str,
                 db_table: str, db_file: str,
                 count: int = -1):
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        if count < 0:
            query = f"UPDATE {db_table} SET {db_column} = {db_column} + 1 WHERE {db_key_column} = ?"
            cursor.execute(query, (key,))
        else:
            query = f"UPDATE {db_table} SET {db_column} = ? WHERE {db_key_column} = ?"
            cursor.execute(query, (count, key))
        conn.commit()  # Commit the transaction
    except sqlite3.Error as e:
        print(f"dbtools: error, updating info count: {e}")
    finally:
        cursor.close()
        conn.close()


# convert info data frame to auto complete class
def infoToAutoComplete(df_info: pd.DataFrame) -> AutoComplete:
    
    words = {}

    for key, row in df_info.iterrows():
        words.update({key: {'key':key}})
        words.update({row['gene']: {'key':key}})
        words.update({row['product']: {'key':key}})
        
        # skip empty note
        if row['note'] == '<note>':
            continue
            
        for note in str(row['note']).split(';'):
            words.update({note: {'key':key}})
    
    ### LOAD COUNTS TO AUTOCOMPLETE ###
    return AutoComplete(words=words)


def matchAutoComplete(search_term: str, auto_complete: AutoComplete) -> list:
    nested_list = auto_complete.search(search_term, 3, 10)
    flat_list = list(set([item for sublist in nested_list for item in sublist]))
    return flat_list


def keyAutoComplete(selected_term: str, auto_complete: AutoComplete) -> str:
    new_count = auto_complete.get_count_of_word(selected_term) + 1
    auto_complete.update_count_of_word(word=selected_term, count=new_count)
    key = auto_complete.words[selected_term]['key']
    return key
