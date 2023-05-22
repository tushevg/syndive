import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from layouts.searchbar import searchbar

def header():

    return html.Div([dmc.Header([
            dmc.Group([
              dmc.Space(w="lg"),
              dmc.Text('SYNDIVE', style={'font-size': '3em', 'font-family': 'DesktopPublishing', 'color':'#9400D3', 'letter-spacing':'0.2em'}),
              dmc.Space(w="lg"),
              dmc.Anchor('About', className='hover-darken', href='about', size='sm', underline=False, weight=300),
              dmc.Anchor('Publications', className='hover-darken', href='publications', size='sm', underline=False, weight=300),
              dmc.Anchor('Dashboard', className='hover-darken', href='dashboard', size='sm', underline=False, weight=300),
              dmc.Anchor('Exports', className='hover-darken', href='exports', size='sm', underline=False, weight=300)], position='left'),
              searchbar()],
              height="10%",
              fixed=True,
              style={"display": "flex", "alignItems": "center",
              "justifyContent": "space-between", "padding": "16px",
              "background": "rgba(255, 255, 255, 0.95)"})
            ])