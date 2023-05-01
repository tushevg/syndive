import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

icon_size = 24
icon_homepage = html.A(href="https://brain.mpg.de/home",
                       children=DashIconify(icon="fluent:brain-circuit-24-regular",
            width=icon_size, height=icon_size, color='black'))

icon_github = html.A(href='https://github.com/tushevg/syndive',
                     children=DashIconify(icon="mdi:github",
                    width=icon_size, height=icon_size, color='black'))

header = dmc.Header(
    height=60,
    style={"display": "flex", "align-items": "center",
    "justify-content": "space-between", "padding": "16px"},
    fixed=True,
    children=[
        dmc.Burger(id="burger-button", opened=False),
        html.H1('Synaptic diversity', style={'color':'#9400D3'}),
        dmc.Group([icon_homepage, icon_github])
    ]
)
