import dash_mantine_components as dmc
from dash import html
import pandas as pd
from layouts.table import table

def text():
    return dmc.Group([
        dmc.Text('How to use the dashboard?', size='xl', color='dark', weight=400),
        dmc.Text('Search for a gene or a protein. Add it to the candidates. Explore its localisation.', size='lg', color='gray', weight=200)
    ], align='center', position='center', spacing='xl', p='2em')


def dashboard(df_info: pd.DataFrame,
              df_enriched: pd.DataFrame,
              df_expressed: pd.DataFrame) -> html.Div:
    return html.Div(className='section',
                    id='dashboard',
                    children=dmc.Stack([text(), table(df_info)],
                            align='center', justify='center', spacing='xl'))
            