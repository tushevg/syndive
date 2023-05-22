import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from layouts.searchbar import searchbar


def logo():
    return dmc.Anchor(dmc.Text('SYNDIVE', 
                    style={'fontSize': '3em', 
                           'fontFamily': 'DesktopPublishing', 
                           'color':'#9400D3', 
                           'letterSpacing':'0.2em'}), href='/', underline=False)


def menu_link(name: str, id: str):
    return dmc.Anchor(name, 
                      className='hover-darken',
                      href=id, 
                      size='md', 
                      underline=False, 
                      weight=200)


def header():
    return html.Div(
        dmc.Header([dmc.Group([logo(),
                               dmc.Space(w='5%'),
                    menu_link('About', 'about'),
                    menu_link('Publications', 'publications'),
                    menu_link('Dashboard', 'dashboard'),
                    menu_link('Exports', 'exports')], 'position', 'left'),
                    searchbar()], 
                  position='top', fixed=True, height="8%",
                  style={"display": "flex", "alignItems": "center",
              "justifyContent": "space-between", "padding": "2%",
              "background": "rgba(255, 255, 255, 0.95)"})
    )
