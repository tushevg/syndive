import dash_mantine_components as dmc
from dash import html
import pandas as pd


def dashboard(df_info: pd.DataFrame,
              df_enriched: pd.DataFrame,
              df_expressed: pd.DataFrame) -> html.Div:
    return html.Div(className='section',
                    id='dashboard',
                    children=dmc.Stack([
                        dmc.Text(df_info.iloc[0,0])
                    ],align='center', justify='center', spacing='xl')
            )
