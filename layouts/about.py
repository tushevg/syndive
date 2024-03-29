import dash_mantine_components as dmc
from dash import html
from layouts.searchbar import searchbar

def title():
    text = 'Synaptic Diversity Hub'
    return dmc.Text(text,
                size='3em',
                weight='bold',
                align='center',
                className='text-gradient')


def summary():
    text = 'A collection of transcripts and proteins localised to neurites and synapses of excitatory and inhibitory neurons. The data is published by the Schuman Lab at MPI for Brain Research.'
    return dmc.Text(text, color='dimmed', align='center', weight='lighter', maw='60%')


def button_left():
    return dmc.Button(dmc.Anchor(dmc.Text('Our science', weight='lighter', color='white'), 
                                 href='https://brain.mpg.de/schuman', underline=False),
                      size='lg', color='dark')


def button_right():
    return dmc.Button(dmc.Anchor(dmc.Text('Learn more', weight='lighter', color='dark'), href='https://brain.mpg.de/home', underline=False),
                      size='lg',
                      color='light',
                      variant='default')


def about():
    return dmc.Container(
        className='section',
        id='id-about',
        fluid=True,
        children=dmc.Stack(
            align='center',
            justify='center',
            spacing='xl',
            maw='80%',
            children=[
                title(),
                dmc.Space(h='5%'),
                summary(),
                dmc.Space(h='5%'),
                searchbar('id-searchbar-about', {'display':'block'}, '80%', '60%'),
                dmc.Space(h='5%'),
                dmc.Group([button_left(), button_right()], position='center')
            ])
    )
