import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

logo_mpibrain = dmc.Image(src='../assets/logo_mpibrain.png', width=100)
logo_scic = dmc.Image(src='../assets/logo_scic.png', width=100)

paper_title='The proteomic landscape of synaptic diversity across brain regions and cell types'
paper_authors='Marc van Oostrum, Thomas Blok, Stefano L. Giandomenico, Susanne tom Dieck, Georgi Tushev, Nicole Fürst, Julian Langer, Erin M. Schuman'
paper_doi='bioRxiv 2023.01.27.525780'
paper_href='https://doi.org/10.1101/2023.01.27.525780'

footer = html.Div([
    dmc.Footer([dmc.Stack([logo_mpibrain, html.Br(),logo_scic]),
                dmc.Stack([
                    dmc.Text(paper_title, size='sm', color='dimmed'),
                    dmc.Text(paper_authors, size='xs', color='dimmed'),
                    dmc.Anchor(paper_doi, href=paper_href, size='xs')
                ]),
                html.Div()],
    height=200,
    style={"display": "flex",
           "alignItems": "center",
           "justifyContent": "space-between"})
])
