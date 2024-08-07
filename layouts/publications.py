import dash_mantine_components as dmc
from dash import html

def text():
    return dmc.Group([
        dmc.Text('What are our resources?', size='xl', color='dark', weight=400),
        dmc.Text('Read how we collect the data. Cite us.', size='lg', color='gray', weight=200)
    ], align='center', position='center', spacing='xl', p='2em')


def paper_card(paper_title: str,
               paper_authors: str,
               paper_journal: str,
               paper_summary: str,
               paper_href: str,
               paper_color: str,
               paper_icon: str):
    return dmc.Card(children=[
            dmc.CardSection(
                dmc.Center([dmc.Image(
                    src=paper_icon,
                    fit='contain',
                    height=200
                )])
            ),
            dmc.Text(paper_title, size='md', weight=500, align='center'),
            dmc.Group(
                [
                    dmc.Text(paper_authors, size='xs', color='dark'),
                    dmc.Badge(dmc.Anchor(paper_journal, inherit=False, href=paper_href, color=paper_color), color=paper_color, variant='light'),
                ],
                position='apart',
                mt='md',
                mb='xs',
            ),
            
            dmc.Text(paper_summary,
                size='xs',
                color='dimmed',
                weight=200
            )
        ],
        withBorder=True,
        shadow='sm',
        radius='md',
        style={'width': 350},
        p='1em'
        )


def cards():
    # Paper 1
    paper_1 = paper_card(
        'The proteomic landscape of synaptic diversity across brain regions and cell types',
        'van Oostrum et al., 2023',
        'Cell',
        'Exploring the proteomic diversity of neuronal synapses, we identify thousands of unique proteins and protein modules associated with specific synapse types.',
        'https://www.sciencedirect.com/science/article/pii/S0092867423010826',
        'blue',
        'assets/fig_mark.png'
    )

    # Paper 2
    paper_2 = paper_card(
        'The translatome of neuronal cell bodies, dendrites, and axons',
        'Glock et. al., 2021',
        'PNAS',
        'Local translation has a substantial contribution to maintain synaptic protein levels and indicates that on-site translational control is an important mechanism to tune synaptic strength.',
        'https://doi.org/10.1073/pnas.2113929118',
        'yellow',
        'assets/fig_caspar.png'
    )

    # Paper 2
    paper_3 = paper_card(
        'The molecular diversity of hippocampal regions and strata at synaptic resolution revealed by integrated transcriptomic and proteomic profiling',
        'Kaulich and Waselenchuk et al., in preparation',
        'bioRxiv',
        'Integrated transcriptomic and proteomic profiling identifies molecular signatures of hippocampal subregions and CA1 strata in tissue and synapses.',
        'https://www.biorxiv.org/content/10.1101/2024.08.05.606570v1',
        'red',
        'assets/fig_kaulich.png'
    )

    return dmc.Group([paper_1, paper_3],
        align="stretch",
        position="center",
        spacing="sm",
        p='2em')
        #style={"width": "90%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"})



def publications():
    return html.Div(className='section',
                    id='publications',
                    children=dmc.Stack([text(),cards()],
                    align='stretch', justify='center', spacing='sm')
            )



