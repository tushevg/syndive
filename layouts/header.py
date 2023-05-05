import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

def header():
    icon_size = 24
    icon_homepage = html.A(href="https://brain.mpg.de/home",
                        children=DashIconify(icon="fluent:brain-circuit-24-regular",
                width=icon_size, height=icon_size, color='black'))

    icon_github = html.A(href='https://github.com/tushevg/syndive',
                        children=DashIconify(icon="mdi:github",
                        width=icon_size, height=icon_size, color='black'))

    return html.Div([dmc.Header([dmc.Burger(id="burger-button", opened=False),
                    dmc.Text('Synaptic diversity', 
                             style={'font-size': '90px', 'font-family': 'DesktopPublishing', 'color':'#9400D3', 'letter-spacing':'10px'}),
                    dmc.Group([icon_homepage, icon_github])],
            height=100,
            style={"display": "flex", "alignItems": "center",
            "justifyContent": "space-between", "padding": "16px"})
            ])
