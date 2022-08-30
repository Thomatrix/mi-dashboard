import pandas as pd


path = "ubicaciones_v2.xlsx" #Cambiar según ubicación y nombre de archivo
dataset = pd.read_excel(path)
dataset=dataset[dataset['Cantidad']!="-"] #Filtrar los -, para poder realizar sumas
