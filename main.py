from numpy import *
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], title='AnimeWreck')
server = app.server

df = pd.read_csv('animes_cleaned.csv')
ind = pd.read_csv('indices.csv')


def load_titles():
    options = []
    for index, row in df.iterrows():
        optdict = {'label': str(row['title']), 'value': str(row['title'])}
        options.append(optdict)
    return options


def get_index_from_name(name):
    return df[df["title"] == name].index.tolist()[0]


def create_card(imgid, titleid, scoreid, moreid):
    card_main = dbc.Card([
        dbc.CardImg(id=imgid, src=df.iloc[0, 10], top=True, bottom=False,
                    title="Image", style={'height': '250px'}),
        dbc.CardBody([
            html.H4(df.iloc[0, 1], id=titleid),
            html.H6(children='Score:', id=scoreid),
            dbc.CardLink('More', id=moreid, href="#")
        ]),
    ],
        color="dark",
        inverse=True,
        outline=False
    )
    return card_main


card0img = dbc.Card([dbc.CardImg(id='img0', src=df.iloc[0, 10], top=True, bottom=False,
                                 title="Image", style={'height': '250px'})],
                    color="dark",
                    inverse=True,
                    outline=False
                    )

card0 = dbc.Card([dbc.CardBody([html.H4(df.iloc[0, 1], className="card-title", id='title0'),
                                html.H6(children='Score:', id='score0'),
                                html.H6(children='Episodes:', id='epi0'),
                                html.H5("Synopsis", className="card-subtitle"),
                                html.P(df.iloc[0, 2], className="card-text", id='syn0', style={'fontSize': 12}),
                                ]),
                  ],
                 color="dark",
                 inverse=True,
                 outline=False
                 )

button = dbc.Row([dbc.Col(dbc.Button("About", color="light", outline=True, id='about', n_clicks=0), width="auto")],
                 no_gutters=True,
                 className="ml-auto flex-nowrap mt-3 mt-md-0",
                 align="center",
                 )

app.layout = html.Div([dbc.Navbar(
    [html.A(dbc.Row(dbc.Col(dbc.NavbarBrand("Anime Recommendation System", className="ml-2", style={'fontSize': 32})),
                    align="center",
                    no_gutters=True)),
     dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
     dbc.Collapse(button, id="navbar-collapse", navbar=True, is_open=False)],
    color="dark",
    dark=True),
    dbc.Row(dbc.Col(dbc.Collapse(
        dbc.Card(dbc.CardBody('Content Based Anime Recommendation System built using Dash in '
                              'Python. It uses machine learning to recommend similar anime. '
                              'Choose an anime from the dropdown button to get your recommendations'),
                 style={'fontSize': 18},
                 color='dark',
                 inverse=True,
                 outline=False),
        id="collapse",
        is_open=False,
    ))),
    dbc.Row(dbc.Col(dcc.Dropdown(id='titleinput',
                                 options=load_titles(),
                                 placeholder='Choose an anime..',
                                 value='Naruto',
                                 multi=False,
                                 searchable=True,
                                 clearable=False,
                                 optionHeight=45,
                                 persistence=True,
                                 persistence_type='session',
                                 ),
                    width={'size': 4, 'offset': 0}
                    ),
            style={'marginBottom': 10, 'marginTop': 10, }
            ),
    dbc.Row([dbc.Col(card0img, width=2),
             dbc.Col(card0, width=10),
             ],
            style={'marginBottom': 20, 'marginTop': 10}
            ),
    dbc.Row(dbc.Col(html.H3('Recommendations')),
            style={'color': 'white'}
            ),
    dbc.Row([dbc.Col(create_card('img1', 'title1', 'score1', 'more1'), width=2),
             dbc.Col(create_card('img2', 'title2', 'score2', 'more2'), width=2),
             dbc.Col(create_card('img3', 'title3', 'score3', 'more3'), width=2),
             dbc.Col(create_card('img4', 'title4', 'score4', 'more4'), width=2),
             dbc.Col(create_card('img5', 'title5', 'score5', 'more5'), width=2),
             dbc.Col(create_card('img6', 'title6', 'score6', 'more6'), width=2)
             ],
            style={'marginBottom': 10, 'marginTop': 0}
            ),
    dbc.Row([dbc.Col(create_card('img7', 'title7', 'score7', 'more7'), width=2),
             dbc.Col(create_card('img8', 'title8', 'score8', 'more8'), width=2),
             dbc.Col(create_card('img9', 'title9', 'score9', 'more9'), width=2),
             dbc.Col(create_card('img10', 'title10', 'score10', 'more10'), width=2),
             dbc.Col(create_card('img11', 'title11', 'score11', 'more11'), width=2),
             dbc.Col(create_card('img12', 'title12', 'score12', 'more12'), width=2)
             ])
])


@app.callback(
    Output("collapse", "is_open"),
    [Input("about", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output(component_id='img0', component_property='src'),
     Output(component_id='title0', component_property='children'),
     Output(component_id='score0', component_property='children'),
     Output(component_id='epi0', component_property='children'),
     Output(component_id='syn0', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback0(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 0]
    epi = 'Episodes: ' + str(df.loc[i]['episodes'])
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score, epi, df.loc[i]['synopsis']


@app.callback(
    [Output(component_id='img1', component_property='src'),
     Output(component_id='title1', component_property='children'),
     Output(component_id='score1', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback1(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 1]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img2', component_property='src'),
     Output(component_id='title2', component_property='children'),
     Output(component_id='score2', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback2(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 2]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img3', component_property='src'),
     Output(component_id='title3', component_property='children'),
     Output(component_id='score3', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback3(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 3]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img4', component_property='src'),
     Output(component_id='title4', component_property='children'),
     Output(component_id='score4', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback4(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 4]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img5', component_property='src'),
     Output(component_id='title5', component_property='children'),
     Output(component_id='score5', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback5(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 5]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img6', component_property='src'),
     Output(component_id='title6', component_property='children'),
     Output(component_id='score6', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback6(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 6]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img7', component_property='src'),
     Output(component_id='title7', component_property='children'),
     Output(component_id='score7', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback7(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 7]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img8', component_property='src'),
     Output(component_id='title8', component_property='children'),
     Output(component_id='score8', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback8(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 8]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img9', component_property='src'),
     Output(component_id='title9', component_property='children'),
     Output(component_id='score9', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback9(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 9]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img10', component_property='src'),
     Output(component_id='title10', component_property='children'),
     Output(component_id='score10', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback10(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 10]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img11', component_property='src'),
     Output(component_id='title11', component_property='children'),
     Output(component_id='score11', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback11(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 11]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    [Output(component_id='img12', component_property='src'),
     Output(component_id='title12', component_property='children'),
     Output(component_id='score12', component_property='children')],
    Input(component_id='titleinput', component_property='value'))
def callback12(title):
    id = get_index_from_name(title)
    i = ind.iloc[id, 12]
    score = 'Score: ' + str(df.loc[i]['score'])
    return df.loc[i]['img_url'], df.loc[i]['title'], score


@app.callback(
    Output(component_id='titleinput', component_property='value'),
    [Input(component_id='more1', component_property='n_clicks'),
     Input(component_id='more2', component_property='n_clicks'),
     Input(component_id='more3', component_property='n_clicks'),
     Input(component_id='more4', component_property='n_clicks'),
     Input(component_id='more5', component_property='n_clicks'),
     Input(component_id='more6', component_property='n_clicks'),
     Input(component_id='more7', component_property='n_clicks'),
     Input(component_id='more8', component_property='n_clicks'),
     Input(component_id='more9', component_property='n_clicks'),
     Input(component_id='more10', component_property='n_clicks'),
     Input(component_id='more11', component_property='n_clicks'),
     Input(component_id='more12', component_property='n_clicks')],
    [State(component_id='title1', component_property='children'),
     State(component_id='title2', component_property='children'),
     State(component_id='title3', component_property='children'),
     State(component_id='title4', component_property='children'),
     State(component_id='title5', component_property='children'),
     State(component_id='title6', component_property='children'),
     State(component_id='title7', component_property='children'),
     State(component_id='title8', component_property='children'),
     State(component_id='title9', component_property='children'),
     State(component_id='title10', component_property='children'),
     State(component_id='title11', component_property='children'),
     State(component_id='title12', component_property='children')],
    prevent_initial_call=True
)
def more1callback(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, title1, title2, title3, title4, title5, title6,
                  title7, title8, title9, title10, title11, title12):
    ctx = dash.callback_context
    n = ctx.triggered[0]['prop_id']
    if n == 'more1.n_clicks':
        return title1
    if n == 'more2.n_clicks':
        return title2
    if n == 'more3.n_clicks':
        return title3
    if n == 'more4.n_clicks':
        return title4
    if n == 'more5.n_clicks':
        return title5
    if n == 'more6.n_clicks':
        return title6
    if n == 'more7.n_clicks':
        return title7
    if n == 'more8.n_clicks':
        return title8
    if n == 'more9.n_clicks':
        return title9
    if n == 'more10.n_clicks':
        return title10
    if n == 'more11.n_clicks':
        return title11
    if n == 'more12.n_clicks':
        return title12


if __name__ == "__main__":
    app.run_server(debug=True)
