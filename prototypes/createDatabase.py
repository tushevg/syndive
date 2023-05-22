import pandas as pd
import sqlite3

def print_table(table: pd.core.frame.DataFrame, label: str):
    print(label)
    print("column name\tdata type")
    for col in table.columns:
        print(f"{col}\t\t{table[col].dtype}")  

# load data frames
table_info = pd.read_csv('data/tableInfo.tsv', sep='\t', index_col=0)
table_expressed = pd.read_csv('data/tableExpressed.csv', sep=',', index_col=0)
table_enriched = pd.read_csv('data/tableEnriched.csv', sep=',', index_col=0)

print_table(table_info, 'info')
print_table(table_expressed, 'expressed')
print_table(table_enriched, 'enriched')

# create database
file_db = 'data/mpibr_synprot.db'
conn = sqlite3.connect(file_db)
table_info.to_sql('info', conn, if_exists='replace', index=True)
table_expressed.to_sql('expressed', conn, if_exists='replace', index=True)
table_enriched.to_sql('enriched', conn, if_exists='replace', index=True)
conn.commit()
conn.close()
