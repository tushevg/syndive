import dash_mantine_components as dmc
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
    return dmc.Stack([dmc.Text(text_institute, align='center', color='dark', weight=300, size='xs'),
                      dmc.Text(text_facility, align='center', color='dark', weight=300, size='xs'),
                      dmc.Text(text_date, align='center', color='dark', weight=300, size='xs')],
                     spacing='xl',
                     align='center',
                     justify='center')


def icons():
    icon_size = 24
    icon_gitlab = dmc.Anchor(
        href="https://gitlab.mpcdf.mpg.de/mpibr",
        children=DashIconify(icon="mdi:gitlab",
            width=icon_size,
            height=icon_size,
            color='black'
        )
    )

    icon_github = dmc.Anchor(
        href='https://github.com/tushevg/syndive',
        children=DashIconify(icon="mdi:github",
            width=icon_size,
            height=icon_size,
            color='black'
        )
    )
    
    return dmc.Group([icon_gitlab, icon_github],
                     spacing='xl',
                     align='center',
                     position='right')


def footer():
    return dmc.Footer(
        id='id-footer',
        height='15%',
        position='bottom',
        children=dmc.Group(
            position='center',
            spacing='xl', 
            grow=True,
            p='4%',
            children=[logos(), text(), icons()],
        )
    )
