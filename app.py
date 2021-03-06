import dash
from dash import dcc, html
from dash.dependencies import Output, Input
from pymongo import MongoClient
import css
import statistics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mamadou_tools
import dash_bootstrap_components as dbc

client = MongoClient()

db = client["Projet_Bachelor"]
sort = {'$sort': {'uniqueCount': -1}}
limitation = {'$limit': 1000}
unique = {"$group": {"_id": "$name", "uniqueCount": {"$max": "$rating"}}}
l = list(db.players.aggregate([unique, sort, limitation]))
players_list = [i['_id'] for i in l]
players_list = [{"label": i.upper(), "value": i} for i in players_list] + [{'label': 'MOYENNE', 'value': 'MOYENNE'}]

avg_age = mamadou_tools.avg_players_age()
max_age = mamadou_tools.max_players_age()
min_age = mamadou_tools.min_players_age()

avg_height = mamadou_tools.avg_players_height()
max_height = mamadou_tools.max_players_height()
min_height = mamadou_tools.min_players_height()

avg_weight = mamadou_tools.avg_players_weight()
max_weight = mamadou_tools.max_players_weight()
min_weight = mamadou_tools.min_players_weight()

position = mamadou_tools.df_player_by_position()
fig = px.pie(position, values='count', names='new_position')
fig.update_layout(
        showlegend=True,
        paper_bgcolor="rgb(0,0,0,0)",
        plot_bgcolor="#1e1e1e",
        template="plotly_dark"
    )




app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('FIFA 22 DATAVIZ', style=css.header_title),
    dcc.Tabs(id="Menu", value='tab-intro', style=css.custom_tabs, children=[
        dcc.Tab(label='INTRODUCTION', value='tab-intro', style=css.custom_tab,
                selected_style=css.custom_tab_selected),
        dcc.Tab(label='PROFIL', value='tab-profil', style=css.custom_tab,
                selected_style=css.custom_tab_selected),
        dcc.Tab(label='NOTATION', value='tab-notes', style=css.custom_tab, selected_style=css.custom_tab_selected),
        dcc.Tab(label="EQUIPES TYPES", value='tab-team', style=css.custom_tab,
                selected_style=css.custom_tab_selected),
    ]),
    html.Div(id='tabs-content-example-graph'),
])


@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('Menu', 'value'),
              suppress_callback_exceptions=True)
def render_content(tab):
    if tab == 'tab-intro':
        return html.Div([
            html.P(
                children="R??alisation d'un tableau de bord sur FIFA ULTIMATE TEAM 22. "
                         "Ce tableau de bord a pour objectif de pr??senter les joueurs pr??sents sur FIFA 22 ainsi que "
                         "la notation qui a ??t?? faite sur ces m??mes joueurs.",
                style=css.font
            )
        ], style=css.background_style)
    elif tab == 'tab-notes':
        return html.Div([
            dcc.Dropdown(
                id='num_multi',
                options=players_list,
                value='MOYENNE',
                style=css.tex_input
            ),
            html.Table([
                html.Tr([html.Td(id='player-name')])
            ], style=css.title_name),
            html.Div([
                html.Table([
                    html.Tr([html.Td(id='given-mean')]),
                    html.Tr([html.Td(['Note G??n??rale donn?? par FIFA'])], style=css.mean_title),
                    html.Tr([html.Td(['T'])], style={'color': '#1E1E1E'}),
                    html.Tr([html.Td(id='calculated-mean')]),
                    html.Tr([html.Td(['Note G??n??rale calcul?? gr??ce ?? la moyenne des notes du joueur'])],
                            style=css.mean_title)
                ], style=css.given_mean),
                dcc.Graph(id='ratings_radar', style=css.radar)
            ], style={'width': '100%', 'padding-top': '2%'}),

        ], style=css.background_style)
    elif tab == 'tab-profil':
        return html.Div([
            html.Table([
                html.Tr([html.Th(" ")]),
                html.Tr([html.Th("AGE"), html.Th("TAILLE"), html.Th("POIDS")], style=css.mean_title),
                html.Tr([html.Th(""), html.Th("MOYENNE"), html.Th("")], style=css.mean_title),
                html.Tr([html.Td(avg_age), html.Td(avg_height), html.Td(avg_weight)]),
                html.Tr([html.Th(""), html.Th("MINIMUM"), html.Th("")], style=css.mean_title),
                html.Tr([html.Td(min_age), html.Td(min_height), html.Td(min_weight)]),
                html.Tr([html.Th(""), html.Th("MAXIMUM"), html.Th("")], style=css.mean_title),
                html.Tr([html.Td(max_age), html.Td(max_height), html.Td(max_weight)])
            ], style=css.tab),

            html.Div([
                dcc.Graph(figure=fig, style={
                    "width": "40%",
                    "display": "inline-block",
                    "overflow": "hidden",
                    "top": "40%",
                    "left": "50%",
                    "margin-top": "0%"
                })
            ])

        ], style=css.background_style)

    elif tab == 'tab-team':
        return html.Div([
            dcc.RadioItems(
                id='display_teams',
                options=[
                    {'label': 'Rating', 'value': 'rating'},
                    {'label': 'Average', 'value': 'average'},
                ],
                value='rating',
                labelStyle={'display': 'inline-block'},
                style=css.custom_radio
            ),
            html.Div([], id='id_div')
        ], style=css.background_style)

@app.callback(Output('id_div', 'children'),
              Input('display_teams', 'value'),
              suppress_callback_exceptions=True)
def team_display(value):
    if value == 'rating':
        return html.Div([ ], style = css.best_team_rating)
    elif value == 'average':

        return html.Div([ ],style = css.best_team_average)


@app.callback(
    Output('given-mean', 'children'),
    Output('calculated-mean', 'children'),
    Output(component_id="ratings_radar", component_property="figure"),
    Output('player-name', 'children'),
    Input('num_multi', 'value'))
def update_output(num_multi):
    true_mean = {"$group":
                     {"_id": "",
                      "given_mean": {"$avg": "$rating"}
                      }
                 }
    mean_ratings = {"$group":
                        {"_id": "",
                         "mean_rating": {"$avg": "$rating"},
                         "mean_pace": {"$avg": "$pace"},
                         "mean_shooting": {"$avg": "$shooting"},
                         "mean_passing": {"$avg": "$passing"},
                         "mean_dribbling": {"$avg": "$dribbling"},
                         "mean_defending": {"$avg": "$defending"},
                         "mean_physicality": {"$avg": "$physicality"},
                         }
                    }
    attributes = ['Rating', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality']
    if num_multi == 'MOYENNE':
        ratings = list(
            db.players.find({}, {"pace": 1, "shooting": 1, "passing": 1, "dribbling": 1, "defending": 1,
                                        "physicality": 1, '_id': 0}))
        given_moy = int(list(db.players.aggregate([true_mean]))[0]['given_mean'])
        ratings_list = [values for key, values in list(db.players.aggregate([mean_ratings]))[0].items()][
                       1:]
    else:
        ratings = list(
            db.players.find({"name": num_multi}, {"pace": 1, "shooting": 1, "passing": 1, "dribbling": 1, "defending": 1,
                                        "physicality": 1, '_id': 0}))
        match_player = {"$match": {"name": str(num_multi)}}
        given_moy = int(list(db.players.aggregate([match_player, true_mean]))[0]['given_mean'])
        ratings_list = [values for key, values in list(db.players.aggregate([match_player, mean_ratings]))[0].items()][
                       1:]
    ratings_values = []
    for items in ratings:
        for key in items:
            ratings_values.append(items[key])
    ratings_moy = int(statistics.mean(ratings_values))

    df = pd.DataFrame(dict(
        r=ratings_list,
        theta=attributes))
    fig = go.Figure(data=go.Scatterpolar(
        r=ratings_list,
        theta=attributes,
        line=dict(color='rgb(197, 244, 87)', width=5),
        fill='toself',
        visible=True,
        textfont=dict(color="rgb(255,255,255)",
                      family="Open Sans",
                      size=5),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False,
        paper_bgcolor="rgb(0,0,0,0)",
        plot_bgcolor="#1e1e1e",
        font=dict(color="rgb(255,255,255)",
                      family="Open Sans",
                      size=15),
        margin=dict(b=15,
                    l=15,
                    r=15,
                    t=15),
        template="plotly_dark"
    )

    return given_moy, ratings_moy, fig, num_multi.upper()

if __name__ == '__main__':
    app.run_server(debug=True)
