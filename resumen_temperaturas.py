#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import os
from tqdm import tqdm


# In[21]:


try:
    os.mkdir('resumenTemperatura')
except:
    None


# In[26]:


for estacion in tqdm(os.listdir('datosTemperatura')):
    archivos = sorted(os.listdir('datosTemperatura/'+estacion))
    
    resumen = pd.read_csv('datosTemperatura/'+estacion+'/'+archivos[0])
    for archivo in archivos[1:]:
        data_aux = pd.read_csv('datosTemperatura/'+estacion+'/'+archivo)
        resumen = pd.concat((resumen, data_aux))
        
    resumen.to_csv('resumenTemperatura/'+estacion+'.csv')

