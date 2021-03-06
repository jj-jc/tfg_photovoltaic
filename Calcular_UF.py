# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Error as E
import plotly.graph_objects as go
import plotly.io as pio
import math
pio.renderers.default='browser'
AOILIMIT=55.0
# VALOR_NORMALIZAR=0.0009180248205304829
VALOR_NORMALIZAR=0.0008882140968826235
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')
df_iam=pd.read_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.csv")
df_iam=df_iam.set_index(df_iam['Unnamed: 0'].values)
df_iam=df_iam.drop('Unnamed: 0',axis=1)

filt_df=df[df['aoi']<=AOILIMIT]
filt_df['DII_efectiva (W/m2)']=filt_df['DII (W/m2)']*E.calc_iam(filt_df['aoi'].values,'Tercer grado')
filt_df['ISC_IIIV/DII_efectiva (A m2/W)']=filt_df['ISC_measured_IIIV (A)']/filt_df['DII_efectiva (W/m2)']
filt_x=filt_df['T_Amb (ºC)'].values
filt_y=filt_df['ISC_IIIV/DII_efectiva (A m2/W)'].values

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,label='Datos de eficiencia de capatación')
plt.plot(filt_df['aoi'],filt_y,'o',markersize=4,label='Datos corregidos por el IAM')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Eficiencia de la parte de III-V una vez corregida la irradiancia con el IAM',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

filt_df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Prueba.csv")

#%% CÓDIGO PARA OBSERVAR LA INFLUENCIA DEL AIRMASS
filt_df_temp=filt_df
# filt_df_temp=filt_df_temp[(filt_df_temp['airmass_relative']>=1.0)]
# filt_df_temp=filt_df_temp[(filt_df_temp['airmass_relative']<1.1)]
Incremento=0.05
Max_airmass=math.ceil(filt_df_temp['airmass_relative'].max())
Min_airmass=math.floor(filt_df_temp['airmass_relative'].min())
fig=go.Figure()
aux=np.arange(Min_airmass,Max_airmass,Incremento)
for i in aux:
    AUX=filt_df_temp[(filt_df_temp['airmass_relative']>=float(i))]
    AUX=AUX[((AUX['airmass_relative'])<(i+Incremento))]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['T_Amb (ºC)'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='airmass '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función de la temperatura ambiente, divido por intervalos de masa de aire",
    xaxis_title="Temperatura (ºC)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
Incremento=0.5
Max_airmass=math.ceil(filt_df_temp['Wind Speed (m/s)'].max())
Min_airmass=math.floor(filt_df_temp['Wind Speed (m/s)'].min())
fig=go.Figure()
aux=np.arange(Min_airmass,Max_airmass,Incremento)
for i in aux:
    AUX=filt_df_temp[(filt_df_temp['Wind Speed (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Speed (m/s)'])<(i+Incremento))]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['T_Amb (ºC)'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='airmass '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Temperatura (ºC)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
Incremento=10
Max_airmass=math.ceil(filt_df_temp['Wind Dir. (m/s)'].max())
Min_airmass=math.floor(filt_df_temp['Wind Dir. (m/s)'].min())
fig=go.Figure()
aux=np.arange(Min_airmass,Max_airmass,Incremento)
for i in aux:
    AUX=filt_df_temp[(filt_df_temp['Wind Dir. (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Dir. (m/s)'])<(i+Incremento))]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['T_Amb (ºC)'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='airmass '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Temperatura (ºC)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
#%% Cálulco UF_temp
filt_df_temp=filt_df
filt_df_temp=filt_df_temp[(filt_df_temp['airmass_relative']>=1.0)]
filt_df_temp=filt_df_temp[(filt_df_temp['airmass_relative']<1.1)]

datos_guardar=pd.DataFrame({'T_Amb (ºC)':filt_df_temp['T_Amb (ºC)'].values,'ISC_IIIV/DII_efectiva (A m2/W)':filt_df_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values})

filt_df_temp_x=filt_df_temp['T_Amb (ºC)'].values
filt_df_temp_y=filt_df_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values/VALOR_NORMALIZAR

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['T_Amb (ºC)'].values,filt_df['ISC_IIIV/DII_efectiva (A m2/W)'].values/VALOR_NORMALIZAR,'o',markersize=4,label='Datos')
plt.plot(filt_df_temp_x,filt_df_temp_y,'o',markersize=4,label='Datos tras filtrado')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (ºC)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Datos escogidos de la nube de puntos',fontsize=40)
plt.legend(fontsize=30,markerscale=3)


y1_regre,RR_temp,a_s1,b1=E.regresion_polinomica(filt_df_temp_x,filt_df_temp_y,1)
fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_temp_x,filt_df_temp_y,'o',markersize=4,label='Datos escogidos')
plt.plot(filt_df_temp_x,y1_regre,'o',markersize=4,label='Línea de regresión')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (ºC)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Cálculo del UF para la temperatura',fontsize=40)
plt.legend(fontsize=30,markerscale=3)
print('El coeficiente de determinación para los datos por debajo de AOILIMIT es de: '+str(RR_temp))

a_temp=a_s1[1]
thld=filt_df_temp_x[np.where(y1_regre==y1_regre.max())]
simple_uf= 1 + (filt_df_temp_x - thld) * (a_temp)
# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_df_temp_x,simple_uf,'o',markersize=4,label='Datos primera parte')
UF_temp=simple_uf
thld_temp=thld[0]

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_temp_x,filt_df_temp_y,'o',markersize=4,label='Datos escogidos')
plt.plot(filt_df_temp_x,simple_uf,'o',markersize=4,label='Línea de regresión')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (ºC)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Cálculo del UF para la temperatura',fontsize=40)
plt.legend(fontsize=30,markerscale=3)


x=filt_df_temp_x.tolist()

x_dibujar=sorted(x)
UF_temp_dibujar=sorted(UF_temp, reverse=True)

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_temp_x,filt_df_temp_y,'o',markersize=4,label='Datos escogidos')
plt.plot(filt_df_temp_x,simple_uf,'-',markersize=4, label='Factor de Utilización')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (ºC)',fontsize=30)
plt.ylabel('Factor de utilización (n.d.)',fontsize=30)
plt.title('Factor de utilización para la temperatura',fontsize=40)
plt.legend(fontsize=30)
#%%CÓDIGO PARA OBSERVAR LAS TENDENDICAS CON TEMPERTAURA, LA VELOCIDAD DEL VIENTO Y DIRECCION DE ESTE 
filt_df=filt_df[filt_df['T_Amb (ºC)']>=19]
filt_df=filt_df[filt_df['T_Amb (ºC)']<22]
Incremento=1
Max_temp=math.ceil(filt_df['T_Amb (ºC)'].max())
Min_temp=math.floor(filt_df['T_Amb (ºC)'].min())
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df[(filt_df['T_Amb (ºC)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['airmass_relative'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()

Incremento=0.1
Max_temp=math.ceil(filt_df['Wind Speed (m/s)'].max())
Min_temp=math.floor(filt_df['Wind Speed (m/s)'].min())
aux_vector=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in aux_vector:
    AUX=filt_df[(filt_df['Wind Speed (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['airmass_relative'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
Incremento=10
Max_temp=math.ceil(filt_df['Wind Dir. (m/s)'].max())
Min_temp=math.floor(filt_df['Wind Dir. (m/s)'].min())
aux_vector=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in aux_vector:
    AUX=filt_df[(filt_df['Wind Dir. (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Dir. (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['airmass_relative'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
# #al observar el scatter, se observan como dos líneas de tendencias, pero no parecen que se la tempera amb 
# # la causa de tales tendencias. Puede ser perfectamente la temperatura de trabajo de la célula, que debido 
# # al viento en unas disipa mejor el calor que en las otras. Aunque es cierto que se filtraron los datos
# # para velocidades menores que 2.5

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['Wind Speed (m/s)'],filt_df['ISC_IIIV/DII_efectiva (A m2/W)'],'o',markersize=4,label='Datos ISC_IIIV/DII_efectiva')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['Wind Dir. (m/s)'],filt_df['ISC_IIIV/DII_efectiva (A m2/W)'],'o',markersize=4,label='Datos ISC_IIIV/DII_efectiva')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()
fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['T_Amb (ºC)'],filt_df['ISC_IIIV/DII_efectiva (A m2/W)'],'o',markersize=4,label='Datos ISC_IIIV/DII_efectiva')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()

# Si dibujamos la ISC_IIIV/DII_efectiva (A m2/W) en función de la dirección del viento, observamos
# que existe una mayor densidad de datos, lo que puede indicar mejora de rendimiento en esa situación

#%% Cálculo del UF_AM
filt_df_am=filt_df
#antes
# filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']>=0.9]
# filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']<1.1]
# filt_df_am=filt_df_am[filt_df_am['T_Amb (ºC)']>=20]
# filt_df_am=filt_df_am[filt_df_am['T_Amb (ºC)']<28]
#editar
filt_df_am=filt_df_am[filt_df_am['T_Amb (ºC)']>=19]
filt_df_am=filt_df_am[filt_df_am['T_Amb (ºC)']<22]


#filtrado para búsqueda de la línea de tendencia:
filtrado_eliminar=filt_df_am[filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)']<0.00085]
filtrado_eliminar=filtrado_eliminar[filtrado_eliminar['airmass_relative']<1.3]                  
filt_df_am=filt_df_am.drop(filtrado_eliminar.index[:],axis=0)

filtrado_eliminar=filt_df_am[filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)']>0.00076]
filtrado_eliminar=filtrado_eliminar[filtrado_eliminar['airmass_relative']>1.44]     
filt_df_am=filt_df_am.drop(filtrado_eliminar.index[:],axis=0)

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['airmass_relative'].values,filt_df['ISC_IIIV/DII_efectiva (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(filt_df_am['airmass_relative'].values, filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)'].values,'o',markersize=4,label='Datos tras el filtrado')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.xlabel('Airmass (n.d.)',fontsize=30)
plt.title('Datos escogidos de la nube de puntos',fontsize=40)
plt.legend(fontsize=30,markerscale=3)
#%% Esto es una prueba, como el airmass es está muy liguado al aoi, puede que este comportamiento
# se defina mejor con una regresión de segundo grado o tercero, como sucede con el IAM.

# x=filt_df['airmass_relative'].values
# y=filt_df['ISC_IIIV/DII (A m2/W)'].values
# yr, RR, a_s, b=E.regresion_polinomica(x, y, 2)

# fig=plt.figure(figsize=(30,15))
# plt.plot(x,y,'o',markersize=4)
# plt.plot(x,yr,'o',markersize=4)
# plt.xticks(fontsize=30)
# plt.yticks(fontsize=30)
# plt.xlabel('airmass (n.d.)',fontsize=30)
# plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
# plt.title('Regresión polinómica de grado 2',fontsize=40)
# plt.legend(fontsize=30,markerscale=3)
# print('El coeficiente de determinación es de: ', str(RR))


#SE OBTIENE UN RR=0.8549227924488301 Y SIN LA NECESIDAD DE THLD NI DE SEGUNDAS REGRESIONES

#HAY QUE BUSCAR UN VALOR PARA NORMALIZAR LOS RESULTADOS, 
#escojo el mayor obtenido tras la regresion

# UF_am_2=yr/VALOR_NORMALIZAR
# UF_am_2_retocado=(1-UF_am_2.max())+UF_am_2
# fig=plt.figure(figsize=(30,15))
# # plt.plot(x,simple_uf,'o',markersize=4,label='Datos primera parte')
# plt.plot(x,UF_am_2,'o',markersize=4,label='De forma polinómica de grado 2')
# plt.plot(x,UF_am_2_retocado,'o',markersize=4,label='De forma polinómica de grado 2 desplazado')
# plt.plot(x, UF_am, 'o', markersize=4, label='De forma lineal')
# plt.xlabel('airmass (n.d.)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Comparación de las dos modelos de UF para el airmass')
# plt.legend()

#%%UN CÓDIGO PARA buscar el más óptimo del airmass
x=filt_df_am['airmass_relative'].values
RR_max=-1
thld=0
a_final_high=0
b_final_high=0
a_final_low=0
b_final_low=0
thlds=np.arange(x.min(),x.max(),0.001)

for j in thlds:
    RR_max_high=-1
    filt_df_low=filt_df_am[filt_df_am['airmass_relative']<=j]
    filt_df_high=filt_df_am[filt_df_am['airmass_relative']>j]
    
    x_low=filt_df_low['airmass_relative'].values
    y_low=filt_df_low['ISC_IIIV/DII_efectiva (A m2/W)'].values/VALOR_NORMALIZAR
    yr_low, RR_low, a_s_low, b_low=E.regresion_polinomica(x_low, y_low, 1)
    y_max=float(yr_low[np.where(yr_low==yr_low.max())])
    
    x_high=filt_df_high['airmass_relative'].values
    x_desplazado=filt_df_high['airmass_relative'].values-j
    y_high=filt_df_high['ISC_IIIV/DII_efectiva (A m2/W)'].values/VALOR_NORMALIZAR  
    
    #y_regresion=mx+b donde la b=y_max
    m=np.arange(-1,-0.001,0.0001)
    # yr_high=pd.DataFrame({'x_desplazado': x_desplazado})
    for i in range(len(m)):
        yr_high=x_desplazado*m[i]+y_max
        # yr_high['M= '+str(m[i])]=y_aux
        RR_high=E.Determination_coefficient(y_high,yr_high)  
        if RR_max_high < RR_high:
            RR_max_high=RR_high           
            y=np.concatenate((y_low,y_high))
            y_regre=np.concatenate((yr_low,yr_high))
            RR=E.Determination_coefficient(y,y_regre)
            if RR_max < RR:
                RR_max=RR
                thld=j
                a_final_high=m[i]
                a_final_low=a_s_low[1]
                b_final_low=b_low
                b_final_high=yr_low.max()+(-thld)*a_final_high
            
filt_df_low=filt_df_am[filt_df_am['airmass_relative']<=thld]
filt_df_high=filt_df_am[filt_df_am['airmass_relative']>thld]

x_low=filt_df_low['airmass_relative'].values
y_low=filt_df_low['ISC_IIIV/DII_efectiva (A m2/W)'].values/VALOR_NORMALIZAR

x_high=filt_df_high['airmass_relative'].values

y_high=filt_df_high['ISC_IIIV/DII_efectiva (A m2/W)'].values/VALOR_NORMALIZAR  

y_producida_low=x_low*a_final_low+b_final_low


y_producida_high=x_high*a_final_high+b_final_high

#%%
fig=plt.figure(figsize=(30,15))
plt.plot(x_low,y_producida_low,'o',markersize=4,label='De forma polinómica de grado 2')
plt.plot(x_high,y_producida_high,'o',markersize=4,label='De forma polinómica de grado 2')
plt.plot(filt_df_am['airmass_relative'],filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)']/VALOR_NORMALIZAR,'o',markersize=4,label='De forma polinómica de grado 2')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('airmass (n.d.)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Comparación de las dos modelos de UF para el airmass',fontsize=40)
plt.legend(fontsize=30,markerscale=3)      

#%%ahora hay que aplicar el método de UF
x=filt_df_am['airmass_relative'].values
y=filt_df_am['ISC_IIIV/DII (A m2/W)'].values

UF_am=[]
for i in range(len(x)):
    if x[i]<=thld:
        aux=1 + ( x[i]- thld) * (a_final_low)
        if (aux>1):
            UF_am.append(1)
        else:
            UF_am.append(aux)

    else:
        UF_am.append(1 + ( x[i]- thld) * (a_final_high))
        
x_dibujar=sorted(x)
UF_am_dibujar=sorted(UF_am, reverse=True)

    
fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_am['airmass_relative'],filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)']/VALOR_NORMALIZAR,'o',markersize=4,label='Datos escogidos')
plt.plot(x_dibujar,UF_am_dibujar,'-',markersize=4,label='Factor de Utilización')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Masa de aire (n.d.)',fontsize=30)
plt.ylabel('Factor de utilización (n.d.)',fontsize=30)
plt.legend(fontsize=30)
plt.title('Factor de utilización para la masa de aire',fontsize=40)

#%%Recojo los UF obtenidos y los guardo en un archivo csv
UF=pd.DataFrame(columns={'UF_am_low','UF_am_high','UF_temp'},index=['a','thld','RR'])
UF['UF_am_low']=[a_final_low,thld,RR_max]
UF['UF_am_high']=[a_final_high,thld,RR_max]
UF['UF_temp']=[a_temp,thld_temp,RR_temp]
UF.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv")

