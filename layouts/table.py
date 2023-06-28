import dash_mantine_components as dmc
from dash import html, dash_table
import pandas as pd
from dash_iconify import DashIconify

def table_body(df: pd.DataFrame) -> html.Tbody:
    df = df.sort_values('gene')
    rows = []
    for key, row in df.iterrows():
        protein = html.Td(dmc.Anchor(dmc.Text(key, align='center'), href=f"https://www.uniprot.org/uniprotkb/{key}/entry"))
        gene = html.Td(dmc.Text(row['gene'], align='center'))
        product = html.Td(dmc.Text(row['product'], align='center', size='sm'))
        action_icon = dmc.ActionIcon(DashIconify(icon="mdi:remove", width=24),
                                                   id={'type':'remove-button', 'index':key}, variant='subtle', color='red', size='sm')
        action = html.Td(dmc.Center(action_icon))
        rows.append(html.Tr([protein, gene, product, action]))

    return html.Tbody(rows, id='table-body')

def table_create(df: pd.DataFrame) -> dmc.Table:
    header = html.Thead(html.Tr([html.Th(dmc.Text('protein', align='center')),
                    html.Th(dmc.Text('gene', align='center')),
                    html.Th(dmc.Text('product', align='center')),
                    html.Th(dmc.Text('edit', align='center'))]), id='table-header')
    body = table_body(df)
    return dmc.Table(id='table-info',
                    verticalSpacing="sm",
                    horizontalSpacing="sm",
                    highlightOnHover=True,
                    children=[header, body])





# def table_df2data(df: pd.DataFrame) -> dict:
#     # reset the index to create a 'protein' column
#     df = df.reset_index().rename(columns={'index': 'protein'})

#     # keep only the columns you need
#     df = df[['protein', 'gene', 'product']]
#     df = df.sort_values('gene')

#     # update proteins to markdown lists
#     df['protein'] = df['protein'].apply(lambda x: f'[{x}](https://www.uniprot.org/uniprotkb/{x}/entry)')

#     return df.to_dict('records')


# def table_create(df: pd.DataFrame) -> dash_table.DataTable:
#     return dash_table.DataTable(
#         id='data-table',
#         columns=[{'name': 'protein', 'id': 'protein', 'presentation': 'markdown'},
#                  {'name': 'gene', 'id': 'gene'},
#                  {'name': 'product', 'id': 'product'}],
#         data=table_df2data(df),
#         row_deletable=True,
#         style_header={'textAlign': 'center', 'fontWeight': 'bold'},
#         style_table={'overflowY': 'scroll'},
#         style_data_conditional=[
#         {'if': {'column_id': 'protein'}, 'textAlign': 'center'},
#         {'if': {'column_id': 'gene'}, 'textAlign': 'center'},
#         {'if': {'column_id': 'product'},'textAlign': 'left'}],
#         style_cell={'border': '0.5px solid lightgrey', 'padding': '6px', 'font-family':'Roboto', 'fontSize': '12px'}
#     )



# def table(df: pd.DataFrame) -> dmc.Table:
#     header = [html.Tr([html.Th(dmc.Text('protein', align='center')),
#                     html.Th(dmc.Text('gene', align='center')),
#                     html.Th(dmc.Text('product', align='center')),
#                     html.Th(dmc.Text('edit', align='center'))])]
#     rows = []
#     action_group = []
#     for key, row in df.iterrows():
        
#         protein = html.Td(dmc.Anchor(dmc.Text(key, align='center'), href=f"https://www.uniprot.org/uniprotkb/{key}/entry"))
#         gene = html.Td(dmc.Text(row['gene'], align='center'))
#         product = html.Td(dmc.Text(row['product'], align='center', size='sm'))
#         action_icon = dmc.ActionIcon(DashIconify(icon="mdi:remove", width=24),
#                                                    id={'index': key, 'type': 'remove-button'}, variant='subtle', color='red', size='sm')
#         action = html.Td(dmc.Center(action_icon))
#         action_group.append(action_icon)
#         rows.append(html.Tr([protein, gene, product, action]))
    
#     return dmc.Table(id='table-info',
#                     verticalSpacing="sm",
#                     horizontalSpacing="sm",
#                     highlightOnHover=True,
#                     children=[html.Thead(header), html.Tbody(rows, id='table-data')])
