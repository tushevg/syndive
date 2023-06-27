import dash_mantine_components as dmc
from dash import html, dash_table
import pandas as pd
from dash_iconify import DashIconify


def table(df: pd.DataFrame) -> dmc.Table:
    header = [html.Tr([html.Th(dmc.Text('protein', align='center')),
                    html.Th(dmc.Text('gene', align='center')),
                    html.Th(dmc.Text('product', align='center')),
                    html.Th(dmc.Text('edit', align='center'))])]
    rows = []
    for key, row in df.iterrows():
        
        protein = html.Td(dmc.Anchor(dmc.Text(key, align='center'), href=f"https://www.uniprot.org/uniprotkb/{key}/entry"))
        gene = html.Td(dmc.Text(row['gene'], align='center'))
        product = html.Td(dmc.Text(row['product'], align='center', size='sm'))
        action = html.Td(dmc.Center(dmc.ActionIcon(DashIconify(icon="mdi:remove", width=24),
                                        title=key, variant='subtle', color='red', size='sm')))
        rows.append(html.Tr([protein, gene, product, action]))
    
    return dmc.Table(id='data-table',
                    verticalSpacing="sm",
                    horizontalSpacing="sm",
                    highlightOnHover=True,
                    children=[html.Thead(header), html.Tbody(rows)])
