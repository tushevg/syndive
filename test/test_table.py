import pandas as pd
from fast_autocomplete import AutoComplete
import re

import sys
sys.path.append('/Users/tushevg/Desktop/syndive')
import layouts.dbtools as db

# prepare data
db_file = 'data/mpibr_synprot.db'
query_list = ['Gad1', 'Gad2', 'Dlg4', 
               'Shank1', 'Psmc1', 'Psmd5', 'Psma7',
               'Psmc2', 'Th']
df_info = db.listToDataFrame(search_list=query_list, db_column='gene',
                             db_table='info', db_file=db_file)
df_enriched = db.listToDataFrame(search_list=df_info.index.to_list(), 
                                 db_column='protein', db_table='enriched', db_file=db_file)
df_expressed = db.listToDataFrame(search_list=df_info.index.to_list(), 
                                  db_column='protein', db_table='expressed', db_file=db_file)
df_info_full = db.tableToDataFrame(db_table='info', db_file=db_file)
ac_info = db.infoToAutoComplete(df_info=df_info_full)

print(len(df_info))

# query by gene name
query_gene = 'Camk2a'
key = db.keyAutoComplete(query_gene, ac_info)
print(query_gene, key)

# update data frame
df_key_info = db.termToDataFrame(search_term=key, db_column='protein', db_table='info', db_file=db_file)
df_key_enriched = db.termToDataFrame(search_term=key, db_column='protein', db_table='enriched', db_file=db_file)
df_key_expressed = db.termToDataFrame(search_term=key, db_column='protein', db_table='expressed', db_file=db_file)


# concatenate rows
df_info = pd.concat([df_info, df_key_info])
df_enriched = pd.concat([df_enriched, df_key_enriched])
df_expressed = pd.concat([df_expressed, df_key_expressed])
print("info", df_info.index.is_unique)
print("enriched", df_enriched.index.is_unique)
print("expressed", df_expressed.index.is_unique)
print(df_expressed.index)


# check json
df_info_json = df_info.to_json()
df_enriched_json = df_enriched.to_json()
df_expressed_json = df_expressed.to_json()

# check if key is present
query_key = 'P24529'
if query_key in df_info.index:
    print('Key Found')


# check error with plot-expressed
data = []
for value, row in df_info.iterrows():
    label = row['gene']
    item = {'value': value, 'label': label}
    data.append(item)
print(data)