# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 19:49:10 2022

@author: tscha
"""
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
from io import BytesIO


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