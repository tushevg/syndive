from dash import Dash, dcc, html, callback, Output, Input, State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from fast_autocomplete import AutoComplete
import json
from typing import Dict

## interact with JSON dictionary
def autocomplete_export(words: Dict[str, Dict[str, str]], file_json: str):
    with open(file_json, "w") as fp:
        json.dump(words , fp)


def autocomplete_load(file_json: str) -> Dict[str, Dict[str, str]]:
    with open(file_json, 'r') as fp:
        words = json.load(fp)
    return words

words = autocomplete_load('data/autocomplete_info.json')
auto_complete = AutoComplete(words=words)


app = Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div([
    dmc.Group([
        dmc.Select(id='search-bar', 
                    placeholder='Search gene or protein',
                    data=[],
                    searchable=True,
                    limit=20,
                    clearable=True,
                    icon=DashIconify(icon="ci:search-magnifying-glass", flip='horizontal')),
        dmc.Text("selected", id='selected-value', size='xl')
    ])
    
],style={"alignItems": "center"})


@app.callback(Output("search-bar", "data"),
          Input("search-bar", "searchValue"))
def search_value(searchValue):
    query = auto_complete.search(word=searchValue, max_cost=3, size=10)
    list = []
    for sublist in query:
        list.append(sublist[-1])
    if (len(list) > 0):
        return list
    else:
        raise PreventUpdate


@callback(Output("selected-value", "children"),
          Input("search-bar", "value"))
def select_value(value):
    if not value:
        raise PreventUpdate
    auto_complete.words[value]['count'] += 1
    auto_complete.update_count_of_word(word=value, count=auto_complete.words[value]['count'])
    #autocomplete_export(auto_complete.words[value])
    gene = auto_complete.words[value]['gene']
    return gene


if __name__ == '__main__':
    app.run_server(debug=True)