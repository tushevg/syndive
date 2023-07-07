import dash_mantine_components as dmc
from dash import html

def title():
    text = 'Synaptic Diversity Hub'
    return dmc.Text(text,
                size='3em',
                weight='bold',
                align='center',
                className='text-gradient')


def summary():
    text = 'A collection of transcripts and proteins localised to neurites and synapses of excitatory and inhibitory neurons. The data is published by the Schuman Lab at MPI for Brain Research.'
    return dmc.Text(text, color='dimmed', align='center', weight='lighter',style={'maxWidth':'60%'})


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
    return html.Div(className='section',
                    id='about',
                    children=dmc.Stack([
                        title(),
                        dmc.Space(h='15%'),
                        summary(),
                        dmc.Space(h='15%'),
                        dmc.Group([button_left(), button_right()], position='center')
                    ],align='center', justify='center', spacing='xl')
            )
