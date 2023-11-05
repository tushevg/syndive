import sqlite3
import pandas as pd
from fast_autocomplete import AutoComplete
import time

import sys
sys.path.append('/Users/tushevg/Desktop/syndive')
import layouts.dbtools as db

db_file='data/mpibr_test.db'
start = time.time()
df = db.termToDataFrame('P11798', 'protein', 'foldchange', db_file)
end = time.time()
print(len(df))
print(df)
print(end - start)


# db_file='data/mpibr_synprot.db'
# df_info = db.tableToDataFrame(db_table='info', db_file=db_file)
# print(len(df_info))
# ac = db.infoToAutoComplete(df_info=df_info)
# list = db.matchAutoComplete('Calm', ac)

# print(list)
# print(len(list))
#print(db.keyAutoComplete('Camk2a', ac))

# query_list = ['Gad1', 'Gad2', 'Dlg4', 
#                'Shank1', 'Psmc1', 'Psmd5', 'Psma7',
#                'Psmc2', 'Th', 'Camk2a']
# query_term = 'P11798'
# df_info = db.listToDataFrame(search_list=query_list,
#                              db_column='gene',
#                              db_table='info',
#                              db_file=db_file)
# print(len(df_info))
# print(df_info.index.to_list())
# print(df_info.loc[query_term])

# db.updateInfoCount(key=query_term, db_column='count', db_key_column='protein',
#                    db_table='info', db_file=db_file)

# df_info = db.termToDataFrame(search_term=query_term,
#                              db_column='protein',
#                              db_table='info',
#                              db_file=db_file)
# print(df_info.loc[query_term])

# db.updateInfoCount(count=0,key=query_term, db_column='count', db_key_column='protein',
#                    db_table='info', db_file=db_file)
