import dash_mantine_components as dmc
from dash import html

def dashboard():
    return html.Div(className='section',
                    id='dashboard',
                    children=dmc.Stack([
                        dmc.Text('DASHBOARD')
                    ],align='center', justify='center', spacing='xl')
            )
