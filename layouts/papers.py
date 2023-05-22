import dash_mantine_components as dmc
from dash import html

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
            dmc.Text(paper_title, weight=500, align='center'),
            dmc.Group(
                [
                    dmc.Text(paper_authors, size='xs', color='dimmed'),
                    dmc.Badge(dmc.Anchor(paper_journal, inherit=False, href=paper_href, color=paper_color), color=paper_color, variant='light'),
                ],
                position='apart',
                mt='md',
                mb='xs',
            ),
            
            dmc.Text(paper_summary,
                size='sm',
                color='dimmed',
            )
        ],
        withBorder=True,
        shadow='sm',
        radius='md',
        style={'width': 350},
        )




def papers():
    # Paper 1
    paper_1 = paper_card(
        'The proteomic landscape of synaptic diversity across brain regions and cell types',
        'van Oostrum et. al., 2023',
        'bioRxiv',
        'Exploring the proteomic diversity of neuronal synapses, we identify thousands of unique proteins and protein modules associated with specific synapse types.',
        'https://doi.org/10.1101/2023.01.27.525780',
        'red',
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

    return dmc.Group([paper_1, paper_2],
        align="stretch",
        position="center",
        spacing="xl",
        style={"width": "90%", "marginTop": 20,"marginBottom": 20, "alignItems": "center"})