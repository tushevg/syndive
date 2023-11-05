import pandas as pd
import sqlite3

def print_table(table: pd.core.frame.DataFrame, label: str):
    print(label)
    print("column name\tdata type")
    for col in table.columns:
        print(f"{col}\t\t{table[col].dtype}")


def create_plain_df(table: pd.DataFrame) -> pd.DataFrame:
    keys = []
    regions = []
    mlines = []
    values = []
    for index, row in table.iterrows():
        for column_name, cell_value in row.items():
            region, mouseline = column_name.split('.', 2)[:2]
            if cell_value != 0:
                keys.append(index)
                regions.append(region)
                mlines.append(mouseline)
                values.append(cell_value)

    return pd.DataFrame({'protein': keys, 
                         'region': regions,
                         'mouseline': mlines,
                         'value': values})

# load data frames
table_info = pd.read_csv('data/tableInfo.tsv', sep='\t', index_col=None)
table_expressed = pd.read_csv('data/tableExpressed.csv', sep=',', index_col=0)
table_enriched = pd.read_csv('data/tableEnriched.csv', sep=',', index_col=0)
table_foldchange = pd.read_csv('data/tableFoldChange.csv', sep=',', index_col=0)

df_enriched = create_plain_df(table_enriched)
df_expressed = create_plain_df(table_expressed)
df_foldchange = create_plain_df(table_foldchange)

table_region = pd.DataFrame(df_expressed['region'].unique(), columns=['name'])
table_mouseline = pd.DataFrame(df_expressed['mouseline'].unique(), columns=['name'])

print(df_enriched)

file_db = 'data/mpibr_test.db'
conn = sqlite3.connect(file_db)
table_info.to_sql('info', conn, if_exists='replace', index=False)
table_region.to_sql('region', conn, if_exists='replace', index=False)
table_mouseline.to_sql('mouseline', conn, if_exists='replace', index=False)
conn.commit()
conn.close()

# info mapping
conn = sqlite3.connect(file_db)
query = "SELECT protein, id FROM info"
info_df = pd.read_sql_query(query, conn)
info_mapping = info_df.set_index('protein')['id'].to_dict()
conn.close()

print(info_mapping)


# file_db = 'data/mpibr_test.db'
# conn = sqlite3.connect(file_db)
# create_table_query = '''
# CREATE TABLE enriched (
#     id INTEGER PRIMARY KEY,
#     info_id INTEGER,
#     region_id INTEGER,
#     mouseline_id INTEGER,
#     value REAL,
#     FOREIGN KEY (info_id) REFERENCES info(id),
#     FOREIGN KEY (region_id) REFERENCES region(id),
#     FOREIGN KEY (mouseline_id) REFERENCES mouseline(id)
# );
# '''
# conn.execute("DROP TABLE IF EXISTS enriched")
# conn.execute(create_table_query)
# conn.commit()

# Map DataFrame values to corresponding IDs from existing tables
# df_enriched['info_id'] = df_enriched['protein'].map(table_info.set_index('protein')['id'])
# df_enriched['region_id'] = df_enriched['region'].map(table_region.set_index('name')['id'])
# df_enriched['mouseline_id'] = df_enriched['mouseline'].map(table_mouseline.set_index('name')['id'])

# print(df_enriched)

# print_table(table_info, 'info')
# print_table(table_expressed, 'expressed')
# print_table(table_enriched, 'enriched')
# print_table(table_foldchange, 'foldchange')

# # create database
# file_db = 'data/mpibr_synprot.db'
# conn = sqlite3.connect(file_db)
# table_info.to_sql('info', conn, if_exists='replace', index=True)
# table_expressed.to_sql('expressed', conn, if_exists='replace', index=True)
# table_enriched.to_sql('enriched', conn, if_exists='replace', index=True)
# table_foldchange.to_sql('foldchange', conn, if_exists='replace', index=True)
# conn.commit()
# conn.close()
