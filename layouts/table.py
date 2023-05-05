import dash_mantine_components as dmc
from dash import html

# create html table
def create_table_info(df):
    center_style = {'textAlign': 'center'}
    #header = [html.Tr([html.Th(col, style=center_style) for col in df.columns])]
    header = [html.Tr([html.Th('protein', style=center_style),
                       html.Th('gene', style=center_style)])]

    rows = []
    for _, row in df.iterrows():
        # Add style to the cells
        protein = row['protein']
        protein = html.Td(dmc.Anchor(protein, href=f"https://www.uniprot.org/uniprotkb/{protein}/entry"), style=center_style)
        gene = html.Td(dmc.HoverCard(
                    withArrow=True,
                    width=200,
                    shadow="md",
                    closeDelay="100ms",
                    children=[
                        dmc.HoverCardTarget(dmc.Text(row['gene'])),
                        dmc.HoverCardDropdown(dmc.Text(row['name'],size="sm"))],
                        style=center_style))
        formatted_row = [protein, gene]
        rows.append(html.Tr(formatted_row))

    table = dmc.Table(id='table-output',
                    verticalSpacing="sm",
                    horizontalSpacing="sm",
                    highlightOnHover=True,
                    children=[html.Thead(header), html.Tbody(rows)])
    return table
