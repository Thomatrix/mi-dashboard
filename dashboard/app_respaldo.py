from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os
from data import gapminder, migrantes
from scatter import get_scatter, get_bubble, get_animated
from heatmap import get_heatmap

from funciones_thomas import get_bubble2, get_words, get_map, get_heat2, sumar_datos, esperanza_vida, get_waffle2
from data_thomas import dataset

import nltk
#%%
is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
if is_gunicorn:
    grupo = os.environ.get("GRUPO", "")
    requests_pathname_prefix = f"/{ grupo }"
else:
    requests_pathname_prefix = "/"

app = Dash(
    __name__,
    requests_pathname_prefix=requests_pathname_prefix,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

app.layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dcc.Dropdown(id="select1", 
                options= [{"label": Categoria_3, "value": Categoria_3} 
                for Categoria_3 in dataset['Categoria 3'].unique()
                ],
                value="Tasa de alfabetización",
                ),
                dbc.Col(
                    dcc.Graph(id="ejercicio1", figure=esperanza_vida(dataset, "Tasa de alfabetización"))
                ),
            ],
            align="center",
        ),
        
    #Mapa de calor
        dbc.Row([
                dcc.Dropdown(id="select2", 
                options= [{"label": continent, "value": continent} 
                for continent in dataset['continent'].dropna().unique()
                ],
                value="South America",
                ),
                
                dbc.Col(
                    dcc.Graph(id="heatmap", figure=get_heat2(sumar_datos(dataset),'South America')) 
                ),
            ],
            align="center",
        ),
        dcc.Dropdown(
                        id="categoria_4", 
                        options= [
                            {"label": Categoria_4, "value": Categoria_4} 
                            for Categoria_4 in dataset['Categoria 4'].unique()
                        ],
                        value="Acceso equitativo",
                    ),

#Mapa mundi
        dbc.Row([
                dbc.Col(
                    dcc.Graph(id="mapa_mundo", figure=get_map(dataset,"Acceso equitativo"))
                ),
            ],
            align="center",
        ),


#Burbuja con linea temporal
        dbc.Row([
                dbc.Col(html.H1("Ejercicio 6"), width=3),
                
                dbc.Col(
                    dcc.Graph(id="ejercicio6", figure=get_bubble2(dataset))
                ),
            ],
            align="center",
        ),
        #Waffle
                dbc.Row([
                dbc.Col(html.H1("Waffle mostrando analfabetismo por país en latinoamerica"), width=12)]
                ),
            html.Div(children=[
                    html.Img(src="data:image/png;base64," + get_waffle2(sumar_datos(dataset)),width='800',height='800')
                ]) ,

#WordCloud
    html.Div(children=[
                    html.Img(src="data:image/png;base64," + get_words(dataset),width='1200',height='600')
                ]) 

    ],
    
    className="p-5",
)


@app.callback(Output("ejercicio1","figure"), Input("select1","value"))

def update_ejercicio1(input1):
    
    return esperanza_vida(dataset, input1)


@app.callback(Output("heatmap","figure"), Input("select2","value"))
def update_ejercicio2(input2):
    
    return get_heat2(sumar_datos(dataset),input2)

@app.callback(Output("mapa_mundo","figure"), Input("categoria_4","value"))
def update_ejercicio3(input3):
    
    return get_map(dataset, input3)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="5000")
