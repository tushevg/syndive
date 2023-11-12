import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback, html, dcc, page_container, State
from dash_iconify import DashIconify

def create_nav_link(name, href):
    return dmc.NavLink(
        children=dmc.Text(name, size='md', weight=200),
        href=href, 
        className='hover-darken'
        )


# raw components
page_links=['About', 'Publications', 'Dashboard', 'Exports']






def create_logo():
    return dmc.Anchor(
        children=dmc.Text('syndive',
                          size='xl', 
                          color='#9400D3',
                          transform='uppercase',
                          ff='DesktopPublishing'),
        href='/',
        underline=False)              


def create_nav_link(name, href):
    return dmc.NavLink(
        children=dmc.Text(name, size='md', weight=200),
        href=href, 
        className='hover-darken'
        )


def create_searchbar(id, style, mw, w):
    return dmc.Select(
        id=id,
        style=style,
        placeholder='Search gene or portein ...',
        data=[],
        maw=mw,
        w=w,
        searchable=True,
        limit=20,
        clearable=True,
        icon=dmc.ThemeIcon(DashIconify(icon="ci:search-magnifying-glass", flip='horizontal'))
    )



def create_header():
    return dmc.Header(
        id='id-header',
        className='header',
        height='8%',
        p = '2%',
        position='top',
        fixed=True,
        children=[
            dmc.Group(
            position='left',
            children=[create_logo(),
                      dmc.Space(w='5%'),
                      create_nav_link('About', '/about'),
                      create_nav_link('Publications', '/publications'),
                      create_nav_link('Dashboard', '/dashboard'),
                      create_nav_link('Exports', '/exports')]),
            dmc.Space(w='5%'),
            create_searchbar('id-searchbar-header', {'display': 'block'}, '25%', '25%')]
        )


def create_side_nav_content():
    return dmc.Stack(
        children=[

        ]
    )


def create_side_navbar():
    return dmc.Navbar(
        fixed=True,
        id="components-navbar",
        position={"top": 70},
        width={"base": 300},
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                children=create_side_nav_content(),
            )
        ],
    )


def create_navbar_drawer():
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayOpacity=0.55,
        overlayBlur=3,
        zIndex=9,
        size=300,
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                style={"height": "100vh"},
                pt=20,
                children=create_side_nav_content(),
            )
        ],
    )



def create_appshell():
    return dmc.MantineProvider(
        dmc.MantineProvider(
            theme={
                "fontFamily": "'Inter', sans-serif",
                "primaryColor": "indigo",
                "components": {
                    "Button": {"styles": {"root": {"fontWeight": 400}}},
                    "Alert": {"styles": {"title": {"fontWeight": 500}}},
                    "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
                },
            },
            inherit=True,
            children=[
                dcc.Store(id="theme-store", storage_type="local"),
                dcc.Location(id="url", refresh="callback-nav"),
                dmc.NotificationsProvider(
                    [
                        create_header(),
                        #create_side_navbar(),
                        #create_navbar_drawer(),
                        html.Div(
                            dmc.Container(size="lg", pt=90, children=page_container),
                            id="wrapper",
                        ),
                    ]
                ),
            ],
        ),
        theme={"colorScheme": "light"},
        id="mantine-docs-theme-provider",
        withGlobalStyles=True,
        withNormalizeCSS=True,
    )


clientside_callback(
    """ function(data) { return data } """,
    Output("mantine-docs-theme-provider", "theme"),
    Input("theme-store", "data"),
)

clientside_callback(
    """function(n_clicks, data) {
        if (data) {
            if (n_clicks) {
                const scheme = data["colorScheme"] == "dark" ? "light" : "dark"
                return { colorScheme: scheme } 
            }
            return dash_clientside.no_update
        } else {
            return { colorScheme: "light" }
        }
    }""",
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)

# noinspection PyProtectedMember
clientside_callback(
    """
    function(children) { 
        ethicalads.load();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return null
    }
    """,
    Output("select-component", "value"),
    Input("_pages_content", "children"),
)

clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "pathname"),
    Input("select-component", "value"),
)

clientside_callback(
    """function(n_clicks) { return true }""",
    Output("components-navbar-drawer", "opened"),
    Input("drawer-hamburger-button", "n_clicks"),
    prevent_initial_call=True,
)