import dash
from dash import dcc
from dash import html
import dash_gif_component as gif
from dash.dependencies import Output, Input
from pymongo import MongoClient
from pprint import pprint
import css
import statistics

client = MongoClient("mongodb+srv://ArielA:ESGI2022@cluster0.na4xebg.mongodb.net/?retryWrites=true&w=majority")

db = client["Projet_Bachelor"]

players_not_gk = {"$match": {"position": {"$ne": "GK"}}}
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
true_mean = {"$group":
                 {"_id": "",
                  "given_mean": {"$avg": "$rating"}
                  }
             }
dic = db.players.find({},{"pace":1, "shooting":1, "passing":1, "dribbling":1, "defending":1, "physicality":1, '_id':0})



print(db.players.find_one({"position": "GK"}))
# print(db.players.)
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('FIFA 22 Dataviz', style=css.header_title),
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
                children="Réalisation d'un tableau de bord sur FIFA ULTIMATE TEAM 22. "
                         "Ce tableau de bord a pour objectif de présenter les joueurs présents sur FIFA 22 ainsi que "
                         "la notation qui a été faite sur ces mêmes joueurs.",
                style=css.font
            )
        ], style=css.background_style)
    elif tab == 'tab-notes':
        return html.Div([

        ], style=css.background_style)


if __name__ == '__main__':
    app.run_server(debug=True)
