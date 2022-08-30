# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 17:22:54 2022

@author: tscha
"""

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import plotly.graph_objects as go
import plotly.express as px

from wordcloud import WordCloud
import base64
from io import BytesIO
import numpy as np
import pandas as pd
from pywaffle import Waffle
import matplotlib.pyplot as plt
#%% Mapa mundo

def get_map(data,categoria_4):   
    
    df=data[data['Categoria 4']==categoria_4].dropna(subset=['Cantidad'])
    if categoria_4=='Acceso equitativo':
        df['Cantidad']=df['Cantidad'].apply(lambda x: 100-float(x))
    df['Cantidad']=df['Cantidad'].apply(lambda x: float(x))
    df=df.rename(columns={'iso_a3':'CODE'})
    
    
    fig = go.Figure(data=go.Choropleth(
        locations = df['CODE'],
        z = df['Cantidad'],
        text = df['País'],
        colorscale = 'Blues',
        #autocolorscale=True,
        #reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Tasa de'+categoria_4,
    ))
    
    fig.update_layout(
        title_text=categoria_4+' mundial',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    return fig
#%% Mapa burbuja y linea temporal

def get_bubble2(data):
    #Tabla 1
    new_data=data[data['Categoria 4']=="Acceso equitativo"]
    df=new_data[['País','Categoria 2','Cantidad','continent']]
    df['Cantidad']=df['Cantidad'].apply(lambda x: float(x))
    col_y='País'
    col_x='Cantidad'
    fig = px.scatter(df, 
                 x=col_x, y=col_y, 
                 animation_frame="Categoria 2", 
                 animation_group="País",
                 size='Cantidad', 
                 color="continent", 
                 hover_name="País", 
                 #title='Acceso a la educación por país',
                 range_y=[0,130] , range_x = [0,100])

    #bubble=fig.show()
    return fig
#%%
def sumar_datos(data):
    new_data=data[data['Categoria 4']=="Acceso equitativo"]
    #new_data=new_data[new_data['Categoria 3']=="Tasa de niños sin escolarizar"]
    
    categorias=["Un año antes de la edad de ingreso a la escuela primaria", "Educación primaria", "Primer ciclo de enseñanza secundaria", "Enseñanza secundaria superior"]
    new_data_sumada=new_data[['País','continent']]
    new_data_sumada
    
    
    for cant in range(len(categorias)):
        print(categorias[cant])
        new_data_1=new_data[new_data['Categoria 2']== categorias[cant]]
        new_data_1=new_data_1[['País','Cantidad']]
        new_data_1['Cantidad']=new_data_1['Cantidad'].apply(lambda x: int(x))
        new_data_1 = pd.pivot_table(new_data_1, index=['País'],values=['Cantidad'],aggfunc=np.mean,fill_value=0)
        new_data_1=new_data_1.rename(columns={"Cantidad":categorias[cant]})
        new_data_sumada=new_data_sumada.merge(new_data_1,how='left',on='País').drop_duplicates()
        
    new_data_sumada=new_data_sumada.dropna()
    return new_data_sumada

#%%
def get_heat2(data,continente):
    
    #continente='South America'
    acceso_seleccionados=data[data.continent==continente]
    #acceso_seleccionados=acceso_seleccionados_1.append(acceso_seleccionados_2)
    acceso_seleccionados.index=acceso_seleccionados['País']
    acceso_seleccionados=acceso_seleccionados.drop(columns=['País','continent'])
    #Grafico de pregunta 1
    fig = px.imshow(acceso_seleccionados,
                    text_auto=True,
                    aspect='auto',
                    labels=dict(x="Países", y="Étapa Escolar", color="Tasa escolaridad"),
                    x=['Preescolar', 'Primaria', 'Secundaria', 'Superior'],
                    y=list(acceso_seleccionados.index)
               )
                    
    return fig

#%% Nube de palabras

# def get_words(data):
#     paises=data[data['Categoria 2']=='Tasa de alfabetización de jóvenes(15 a 24 años) (%)']
#     paises=paises[['País','Cantidad']].drop_duplicates()
#     text=""
#     for i in paises.index:
#         texto_temporal=paises['País'][i].replace(" ","_")
#         for j in range(100-int(paises['Cantidad'][i])):
#             text=text+", "+texto_temporal
#     from nltk.corpus import stopwords
#     nltk.download("stopwords")
    
    
#     stopwords = set(stopwords.words('spanish')) 

#     wc = WordCloud(collocations=False,stopwords=stopwords, background_color="white").generate(text)
#     wc_img = wc.to_image()
#     with BytesIO() as buffer:
#         wc_img.save(buffer, 'png')
#         img2 = base64.b64encode(buffer.getvalue()).decode()     
#     #plt.show()
#     return img2

#%% Esperanza de vida
def esperanza_vida(data,categoria):
    #Seleccionador categoria 3
    df=data[data['Categoria 3']==categoria]
    df=df[['País','Categoria 2','Cantidad','continent','lifeExp','pop_est']]
    
    df['Cantidad']=df['Cantidad'].apply(lambda x: float(x))
    df=df.rename(columns={'Cantidad':categoria,'lifeExp':'Esperanza de vida'})
    
    col_y='Esperanza de vida'
    col_x=categoria
    
    fig = px.scatter(df, 
                     x=col_x, y=col_y, 
                     #size='pop_est', 
                     color="continent", 
                     hover_name="País", 
                     title= col_x +" vs " + col_y)
    return fig
          #range_y=[40,85] , range_x = [25,105])
          
#%% Waffle
def get_waffle2(data_sumada):
    data_sumada=data_sumada[data_sumada.continent=='South America']
    
    data_sumada=data_sumada[['País','Educación primaria']].dropna()
    data_sumada=data_sumada.dropna(subset=['Educación primaria'])
    data_sumada=data_sumada.set_index("País")  #, inplace=True)
    #print(data_sumada)


# imprimir proporciones
    #for i, proportion in enumerate(category_proportions):
        #print (data_sumada.index.values[i] + ': ' + str(proportion))
    plt.figure(
        FigureClass=Waffle, 
        rows=20, 
        columns=20,
        values=list(data_sumada['Educación primaria']),
        
        figsize=(20, 20),
        legend={
        'labels':list(data_sumada.index),
        # 'labels': [f"{k} ({v}%)" for k, v in data.items()],  # lebels could also be under legend instead
        #'loc': 'lower left',
        #'bbox_to_anchor': (0, 1),
        #'ncol': len(data_sumada),
        #'framealpha': 0.2,
        'fontsize': 24
    }
    )
    buf = BytesIO()
    plt.savefig(buf, format = "png") # save to the above file object
    plt.close()
    img3 = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    return img3

#%% Comparador paises
def get_comparador_paises(new_data_sumada,pais1,pais2):
    acceso_seleccionados=new_data_sumada.drop(columns=['continent'])
    #pais1='Albania'
    #pais2='Yemen'
    acceso_seleccionados_1=acceso_seleccionados[acceso_seleccionados['País']==pais1]
    acceso_seleccionados_2=acceso_seleccionados[acceso_seleccionados['País']==pais2]
    acceso_seleccionados=acceso_seleccionados_1.append(acceso_seleccionados_2)
    
    #Grafico de pregunta 1
    fig = px.bar(acceso_seleccionados,
                 title="Tasa de problemas en acceso a la educación por nivel entre 2 países",
                 x="País",
                 y=list(acceso_seleccionados.columns)
    )
    return fig



        