import pandas as pd
import os

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from tqdm import tqdm
from numpy import nan


def temperatura_mensual(estacion, annio, mes):
    '''
    Esta funcion devuelve los datos mensuales de cierta estacion
    metereologica.
    Args:
        estacion (int): Codigo nacional de la estacion metereologica
        annio (int): Annio del que se obtendran datos
        mes (int): Mes del que se obtendran datos
    '''
    urlBase = 'https://climatologia.meteochile.gob.cl/application/mensual/temperaturaMediaMensual/'

    while True:
        i = 0
        try:
            html = urlopen(urlBase+str(estacion)+'/'+str(annio)+'/'+str(mes))
            break

        except HTTPError as e:
            i += 1

        if i > 10:
            break

    bs = BeautifulSoup(html.read(), 'html.parser')

    dataMensual = pd.DataFrame(columns=['Annio', 'Mes', 'Dia', 'Tminima',
                                 'Tmaxima', 'MediaClimatologica',
                                 'MediaAritmetica', 'Datos'])

    i=0
    for dia in bs.findAll('tr', {'class': 'text-center'}):
        dataDia = [annio, mes]

        k=0
        for columna in dia.findAll('td'):
            if k in [0,1,3,5,6,7]:
                dataDia.append(columna.get_text()[1:-1])
            k += 1

        if len(dataDia) > 2:
            dataMensual.loc[i] = dataDia
            i += 1
        else:
            break

    return dataMensual.replace('.', nan)


estaciones = pd.read_csv('CatastroEstaciones.csv')['Codigo Nacional']

carpeta = 'datosTemperatura'

try:
    os.mkdir(carpeta)
except:
    None

for estacion in tqdm(estaciones[500:], leave=False, desc='Estaciones'):
    try:
        os.mkdir(carpeta+'/'+str(estacion))
    except:
        None

    for annio in tqdm(range(2010, 2023), leave=False, desc='Annios'):
        for mes in range(1,13):

            archivo = str(annio)+'-'+str(mes).zfill(2)+'.csv'
            if archivo in os.listdir(carpeta+'/'+str(estacion)+'/'):
                continue

            dataMensual = temperatura_mensual(estacion, annio, mes)

            if len(dataMensual) > 0:
                dataMensual.to_csv(carpeta+'/'+str(estacion)+'/'+archivo,
                                  index=False)
