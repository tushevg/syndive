import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
import datetime


def logos():
    logo_mpibrain = dmc.Anchor(dmc.Image(src='../assets/logo_mpibrain.png', width=100), href='https://brain.mpg.de/home')
    logo_scic = dmc.Anchor(dmc.Image(src='../assets/logo_scic.png', width=100), href='https://brain.mpg.de/computing')
    return dmc.Group([logo_mpibrain, logo_scic], 
                     spacing='xl',
                     align='center',
                     position='left')


def text():
    text_institute = 'Max Planck Institute for Brain Research'
    text_facility = 'Scientific Computing and Data Visualization Facility'
    current_date = datetime.datetime.now()
    text_date = current_date.strftime("%B %Y")
    return dmc.Stack([dmc.Text(text_institute, color='dark', weight=300, size='xs'),
                      dmc.Text(text_facility, color='dark', weight=300, size='xs'),
                      dmc.Text(text_date, color='dark', weight=300, size='xs')],
                     spacing='xl',
                     align='center',
                     justify='center')


def icons():
    icon_size = 24
    icon_gitlab = html.A(href="https://gitlab.mpcdf.mpg.de/mpibr",
                        children=DashIconify(icon="mdi:gitlab",
                width=icon_size, height=icon_size, color='black'))

    icon_github = html.A(href='https://github.com/tushevg/syndive',
                         children=DashIconify(icon="mdi:github",
                        width=icon_size, height=icon_size, color='black'))
    
    return dmc.Group([icon_gitlab, icon_github],
                     spacing='xl',
                     align='center',
                     position='right')


def footer():
    return html.Div(dmc.Footer([
        dmc.Group([logos(), text(), icons()],
                  position='center', spacing='xl', 
                  grow=True, style={'margin':'4em'})],
                height='15%',
                position='bottom',
                ))
