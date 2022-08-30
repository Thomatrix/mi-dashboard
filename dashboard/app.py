from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os
#from data import gapminder, migrantes


from funciones_thomas import get_bubble2, get_map, get_heat2, sumar_datos, esperanza_vida, get_waffle2,get_comparador_paises #get_words
from data_thomas import dataset

#import nltk
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





# app.layout = dbc.Container(
#     children=[
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                     html.H1("Ejercicio 1"), 
#                     dcc.Dropdown(
#                         id="select1", 
#                         options= [
#                             {"label": year, "value": year} 
#                             for year in gapminder.year.unique()
#                         ],
#                         value=2007,
#                     ),
#                 ],
#                 width=3
#                 ),
#                 dbc.Col(
#                     dcc.Graph(id="ejercicio1", figure=get_scatter(gapminder, 2007))
#                 ),
#             ],
#             align="center",
#         ),





app.layout = dbc.Container(
    children=[
        dbc.Row(
            [   html.H1("DASHBOARD - Proyecto Visualización de Datos "), 
                html.H4("Data del ámbito EDUCACIÓN, UNICEF "), 
                dbc.Col(
                    [
                    html.H4("Esperanza de vida vs alfabetización general"), 
                    dcc.Dropdown(
                        id="select1", 
                        options= [
                            {"label": Categoria_3, "value": Categoria_3} 
                            for Categoria_3 in dataset['Categoria 3'].unique()
                ],
                value="Tasa de alfabetización",
                    ),
                    ],
                width=3
                ),
                dbc.Col(
                    dcc.Graph(id="ejercicio1", figure=esperanza_vida(dataset, "Tasa de alfabetización"))
                ),
            ],
            align="center",
        ),
        
    #Mapa de calor
        dbc.Row(
            [
                html.H4("Comparación de tasa de escolaridad por niveles entre países de un mismo continente"), 
                dbc.Col(
                    [
                    html.H6("Seleccione el continente que desea visualizar: "), 
                    dcc.Dropdown(
                        id="select2", 
                        options= [
                            {"label": continent, "value": continent} 
                            for continent in dataset['continent'].dropna().unique()
                ],
                value="South America",
                ),
                ],
                width=3
                ),
                
                dbc.Col(
                    dcc.Graph(id="heatmap", figure=get_heat2(sumar_datos(dataset),'South America')) 
                ),
            ],
            align="center",
        ),
        

#Mapa mundi
        dbc.Row([
            dbc.Col(
                    [
                        html.H6("Seleccione un nivel para visualizar en el MapaMundi: "), 
                    dcc.Dropdown(
                        id="categoria_4", 
                        options= [
                            {"label": Categoria_4, "value": Categoria_4} 
                            for Categoria_4 in dataset['Categoria 4'].unique()
                        ],
                        value="Acceso equitativo",
                    ),
                    ],
                width=3,
                ),

                dbc.Col(
                    dcc.Graph(id="mapa_mundo", figure=get_map(dataset,"Acceso equitativo")), width=9,
                ),
            ],
            align="center",
        ),


#Burbuja con linea temporal
        dbc.Row([
                
                html.H4("Acceso a la Educación por País"), 
                dbc.Col(
                    dcc.Graph(id="bubble", figure=get_bubble2(dataset))
                ),
            ],
            align="center",
        ),




        # #Waffle
        #         dbc.Row([
        #             html.H4("Waffle mostrando analfabetismo por país en latinoamerica"),
                
        #         html.Div(children=[
        #             html.Img(src="data:image/png;base64," + get_waffle2(sumar_datos(dataset)),width='800',height='800')
        #         ]) ,
        #         ]
        #         ),





        #Waffle
        dbc.Row([
            html.H4("Waffle: Problemas de alfabetización por país en latinoamerica"),
            html.Img(src="data:image/png;base64," + get_waffle2(sumar_datos(dataset)),width='600',height='650')
    
        ]
        ),
            

#WordCloud
#     html.Div(children=[
#                     html.Img(src="data:image/png;base64," + get_words(dataset),width='1200',height='600')
#                 ])

        dbc.Row([
                
                #html.H4("Comparador entre paises"),
                dbc.Col(
                    [
                        html.H6("País 1: "), 
                    dcc.Dropdown(
                        id="pais1", 
                        options= [
                            {"label": pais1, "value": pais1} 
                            for pais1 in sumar_datos(dataset)['País'].unique()
                        ],
                        value="Chile",
                    ),
                    ],
                width=3,
                ),
                dbc.Col(
                    [
                        html.H6("País 2: "), 
                    dcc.Dropdown(
                        id="pais2", 
                        options= [
                            {"label": pais2, "value": pais2} 
                            for pais2 in sumar_datos(dataset)['País'].unique()
                        ],
                        value="Uruguay",
                    ),
                    ],
                width=3,
                ),
                dbc.Col(
                    dcc.Graph(id="comparador_paises", figure=get_comparador_paises(sumar_datos(dataset),'Chile','Uruguay')) 
                ),
            ],
            align="center",
        )

 

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

@app.callback(Output("comparador_paises","figure"), Input("pais1","value"),Input("pais2","value"))
def update_ejercicio4(input4,input5):
    
    return get_comparador_paises(sumar_datos(dataset),input4,input5) 

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="5000")
