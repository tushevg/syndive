import dash_mantine_components as dmc
from dash import html

def text():
    return dmc.Group([
        dmc.Text('Do you want to use our data?', size='xl', color='dark', weight=400),
        dmc.Text('Export csv tables. Cite us.', size='lg', color='gray', weight=200)
    ], align='center', position='center', spacing='xl', p='2em')



def exports():
    return html.Div(className='section',
                    id='exports',
                    children=dmc.Stack([
                        text(),
                        dmc.RadioGroup(
                            id="id-radiogroup-export",
                            value="table",
                            label=dmc.Text("Select exporter type", size='lg', color='gray', weight=200),
                            size="sm",
                            mt=10,
                            children=[dmc.Radio(dmc.Text('table', size='lg', color='gray', weight=200), value='table'),
                                      dmc.Radio(dmc.Text('raw data', size='lg', color='gray', weight=200), value='raw')]
                        ),
                        dmc.Group([
                            dmc.Button('info', size='lg', color='dark', id={'type':'export-button', 'index':'export-info'}),
                            dmc.Button('abundance', size='lg', color='light', variant='default', id={'type':'export-button', 'index':'export-abundance'}),
                            dmc.Button('enrichment', size='lg', color='dark', id={'type':'export-button', 'index':'export-enrichment'})
                        ]),
                        dmc.Text('van Oostrum et. al., Cell, 2023', size='lg', color='gray', weight=200, id='debug-export'),
                    ],align='center', justify='center', spacing='xl')
            )