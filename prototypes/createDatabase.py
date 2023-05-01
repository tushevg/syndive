import pandas as pd
import sqlite3

def print_table(table: pd.core.frame.DataFrame, label: str):
    print(label)
    print("Column Name\tData Type")
    print("------------------------")
    for col in table.columns:
        print(f"{col}\t\t{table[col].dtype}")  

# load data frames
table_info = pd.read_csv('data/tableInfo.tsv', sep='\t', index_col=0)
table_expressed = pd.read_csv('data/tableExpressed.csv', sep=',', index_col=0)
table_enriched = pd.read_csv('data/tableEnriched.csv', sep=',', index_col=0)

#print_table(table_info, 'info')
#print_table(table_expressed, 'expressed')
#print_table(table_enriched, 'enriched')

# create database
file_db = 'data/mpibr_synprot.db'
conn = sqlite3.connect(file_db)
table_info.to_sql('info', conn, if_exists='replace', index=True)
table_expressed.to_sql('expressed', conn, if_exists='replace', index=True)
table_enriched.to_sql('enriched', conn, if_exists='replace', index=True)
conn.commit()
conn.close()




# # arguments
# file_data = 'data/tableDeseq_cortex_L1vsL2-6_withFPKM.txt'
# file_db = 'data/rnaseq_cortex.db'
# table_name = 'deseq'

# # read table to panda dataframe
# table_deseq = pd.read_csv(file_data, 
#                           sep='\t',
#                           index_col=0,
#                           usecols=['gene', 'log2FoldChange', 'baseMean', 'padj', 'label'],
#                           dtype={'gene':'string', 
#                                  'log2FoldChange':'float64', 
#                                  'baseMean':'float64',
#                                  'padj':'float64',
#                                  'label':'string'})
# table_deseq.rename(columns={'log2FoldChange':'fold change', 
#                             'baseMean':'expression',
#                             'padj':'p-value',
#                             'label':'enrichment'},
#                             inplace=True)

# Create a connection to a new SQLite3 database
# sqlite3 types are infered from data frame dtype
# column_types = {
#     'gene': 'TEXT',
#     'fold change': 'REAL',
#     'expression': 'REAL',
#     'p-value': 'REAL',
#     'enrichment': 'TEXT'
# }
# conn = sqlite3.connect(file_db)
# table_deseq.to_sql(table_name, conn, if_exists='replace', index=True, dtype=column_types)
# conn.commit()
# conn.close()

