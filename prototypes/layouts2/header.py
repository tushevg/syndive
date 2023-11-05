import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from layouts2.searchbar import searchbar

def logo():
    return dmc.Anchor(dmc.Text('SYNDIVE', 
                    style={'fontSize': '3em', 
                           'fontFamily': 'DesktopPublishing', 
                           'color':'#9400D3', 
                           'letterSpacing':'0.2em'}), href='/', underline=False)


def menu_link(name: str, id: str):
    return html.A(dmc.Text(name, size='md', weight=200), className='hover-darken', href=id)


def header():
    return dmc.Header(
                id='id-header',
                height='8%',
                p = '2%',
                position='top',
                fixed=True,
                className='header', 
                children=[
                    dmc.Group([
                        logo(),
                        dmc.Space(w='5%'),
                        menu_link('About', '#about'),
                        menu_link('Publications', '#publications'),
                        menu_link('Dashboard', '#dashboard'),
                        menu_link('Exports', '#exports')
                    ], 'position', 'left'),
                    searchbar('id-searchbar-header', {'display': 'none'}, '25%')
                ]
            )