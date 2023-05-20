import dash_mantine_components as dmc
from dash import html

def about():
    title = 'Synaptic Diversity Hub'
    summary = 'A collection of transcripts and proteins localised to neurites and synapses of excitatory and inhibotory neurons. The data is published by the Schuman Lab at MPI for Brain Research.'
    return dmc.Stack([
        dmc.Text(title,
                 align='center',
                 className='text-gradient',
                 style={'font-size':60,'font-family': 'Roboto', 'font-weight':'bold'}),
        dmc.Text(summary, align='center', size='xl')
    ],
    style={"width": '60%'},
    align="stretch",
    justify="center",
    spacing="xl")