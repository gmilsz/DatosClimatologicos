import pandas as pd
import os
from tqdm import tqdm


try:
    os.mkdir('resumenTemperatura')
except:
    None


for estacion in tqdm(os.listdir('datosTemperatura')):
    archivos = sorted(os.listdir('datosTemperatura/'+estacion))

    resumen = pd.read_csv('datosTemperatura/'+estacion+'/'+archivos[0])
    for archivo in archivos:
        data_aux = pd.read_csv('datosTemperatura/'+estacion+'/'+archivo)
        resumen = pd.concat((resumen, data_aux))

    if len(resumen) > 1:
    	resumen.to_csv('resumenTemperatura/'+estacion+'.csv', index=False)
