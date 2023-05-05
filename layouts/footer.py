import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
import datetime

def footer():
    logo_mpibrain = dmc.Image(src='../assets/logo_mpibrain.png', width=100)
    logo_scic = dmc.Image(src='../assets/logo_scic.png', width=100)
    text_institute = 'Max Planck Institute for Brain Research'
    text_facility = 'Scientific Computing and Data Visualization Facility'
    current_date = datetime.datetime.now()
    text_date = current_date.strftime("%B %Y")
    
    return html.Div([dmc.Footer([
                        dmc.Stack([logo_mpibrain, html.Br(),logo_scic]),
                        dmc.Stack([dmc.Text(text_institute, size='xs', color='dimmed'),
                                   dmc.Text(text_facility, size='xs', color='dimmed'),
                                   dmc.Text(text_date, size='xs', color='dimmed')],
                                   spacing="xs"),
                        html.Div()
                        ],
                        height=200,
                        style={"display": "flex",
                                "alignItems": "center",
                                "justifyContent": "space-between"})
                        ])

