import dash_mantine_components as dmc
from dash import html

def exports():
    return html.Div(className='section',
                    id='exports',
                    children=dmc.Stack([
                        dmc.Text('EXPORTS')
                    ],align='center', justify='center', spacing='xl')
            )