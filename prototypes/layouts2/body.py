import dash_mantine_components as dmc

from layouts2.about import about
from layouts2.publications import publications

def body():
    return dmc.Container(
        id='id-body',
        fluid=True,
        children=[
            about(),
            publications()
        ]
    )