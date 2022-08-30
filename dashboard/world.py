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

#%% Mapa mundo

def get_map(data):   
    df=data[data['Categoria 4']=="Acceso equitativo"]
    df['Cantidad']=df['Cantidad'].apply(lambda x: float(x))
    df=df.rename(columns={'iso_a3':'CODE'})
    
    
    fig = go.Figure(data=go.Choropleth(
        locations = df['CODE'],
        z = df['Cantidad'],
        text = df['País'],
        colorscale = 'Reds',
        #autocolorscale=True,
        #reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Tasa de analfabetismo',
    ))
    
    fig.update_layout(
        title_text='Analfabetismo mundial',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
#%% Mapa burbuja y linea temporal

def get_bubble2(data):
    #Tabla 1
    new_data=data[data['Categoria 4']=="Acceso equitativo"]
    df=new_data[['País','Categoria 2','Cantidad']]
    df['Cantidad']=df['Cantidad'].apply(lambda x: float(x))
    col_y='País'
    col_x='Cantidad'
    fig = px.scatter(df, 
                 x=col_x, y=col_y, 
                 animation_frame="Categoria 2", 
                 animation_group="País",
                 size='Cantidad', 
                 #color="continent", 
                 hover_name="País", 
                 title='PIB per capita vs Nacimiento de mujeres, en el tiempo',
                 range_y=[0,130] , range_x = [0,100])

    #bubble=fig.show()
    return fig

#%% Nube de palabras

def get_words(data):
    paises=data[data['Categoria 2']=='Tasa de alfabetización de jóvenes(15 a 24 años) (%)']
    paises=paises[['País','Cantidad']].drop_duplicates()
    text=""
    for i in paises.index:
        texto_temporal=paises['País'][i].replace(" ","_")
        for j in range(100-int(paises['Cantidad'][i])):
            text=text+", "+texto_temporal
    from nltk.corpus import stopwords
    #nltk.download("stopwords")
    
    
    stopwords = set(stopwords.words('spanish')) 

    wc = WordCloud(collocations=False,stopwords=stopwords, background_color="white").generate(text)
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()     
    #plt.show()
    return img2