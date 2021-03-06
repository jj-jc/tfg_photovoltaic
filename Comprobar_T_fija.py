# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:45:56 2020

@author: juanj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pvlib
import Error as E
import IAM_ashrae
import IAM_physical_bruto
import IAM_Martin
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')
#se introduce euna columna aue corresponde al index al escribir
df=df.set_index(pd.DatetimeIndex(df['Date Time']))
df=df.drop(['Date Time'],axis=1)
#filtramos el date frame en función del aoi para que las funciones de cálculo del IAM no de valores nan además 
#de que los valores en aois altos no son representativos para el la parte de III-V

df=df[(df['aoi']<55)]


##Se limita la temperatura para que esta no afecte al estudio de los datos en función del ángulo
#Media_temp=df['T_Amb (ºC)'].mean()
#df=df[(df['T_Amb (ºC)']<Media_temp+3)]
#df=df[(df['T_Amb (ºC)']>Media_temp-3)]
#


###Se limita la temperatura 
#df=df[(df['T_Amb (ºC)']<21.0)]
#df=df[(df['T_Amb (ºC)']>=20.0)]

#df=filt_df4
filt_df2=df






#--------------------se calcula el iam en funcion de isc/dii normalizado------------

df['IAM_aoi_']=(df['ISC_IIIV/DII (A m2/W)'])/(df['ISC_IIIV/DII (A m2/W)'].max())

#-------------------datos obtenidos para parametros de funciones de iam-----------------
b=1.1779999732971191
n=0.9000000357627869
k=10.900008201599121
l=0.10000000149011612
a_r=3140001.0
#--------------probamos con los parametros obtenidos y con la normalizacion del isc/DII--------------------------------
y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
y_physical=np.array(pvlib.iam.physical(aoi=df['aoi'], n=n,K=k, L=l))
y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=a_r))
y_poli,RR_poli,a_poli,b_poli=E.regresion_polinomica(df['aoi'],df['IAM_aoi_'],2)


RR_physical=E.Determination_coefficient(df['IAM_aoi_'],y_physical)
RR_ashrae=E.Determination_coefficient(df['IAM_aoi_'],y_ashrae)
RR_martin=E.regresion_lineal(df['IAM_aoi_'],y_martin_ruiz)



plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['IAM_aoi_'],'o',markersize=2,label='todos los datos')
plt.plot(df['aoi'],y_physical,'o',markersize=2,label='regresion por funcion physical')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='regresion por función ashrae')
plt.plot(df['aoi'],y_martin_ruiz,'o',markersize=2,label='regresión por función Martin_Ruiz')
plt.plot(df['aoi'],y_poli,'o',markersize=2,label='regresión por función polinómica')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('IAM')
plt.title("Regresiones de diferentes funciones para el coeficiente de utilización en función del ángulo de incidencia",fontsize=20)
#plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para Martin es:  ' + str(RR_martin)[:str(RR_martin).find(".")+5])
print('El valor del parámetro ar usado es:  ' + str(a_r)[:str(a_r).find(".")+5])


#-----------------fitting con los datos de normalizacion de ISC/DII------------
y_ashrae,RR_ashrae,b=IAM_ashrae.regresion_ashrae(df['aoi'],df['IAM_aoi_'])
y_physical,RR_physical,n,k,l =IAM_physical_bruto.regresion_physical(df['aoi'],df['IAM_aoi_'])
y_martin_ruiz,RR_martin_ruiz,a_r=IAM_Martin.regresion_martin_ruiz(df['aoi'],df['IAM_aoi_'])
y_poli,RR_poli,a_poli,b_poli=E.regresion_polinomica(df['aoi'],df['IAM_aoi_'],2)

#y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
#y_physical=np.array(pvlib.iam.physical(aoi=np.array(df['aoi']),n=n,K=k,L=l))
#y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=a_r))

plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['IAM_aoi_'],'o',markersize=2,label='todos los datos')
plt.plot(df['aoi'],y_physical,'o',markersize=2,label='regresion por funcion physical')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='regresion por función ashrae')
plt.plot(df['aoi'],y_martin_ruiz,'o',markersize=2,label='regresión por función Martin_Ruiz')
plt.plot(df['aoi'],y_poli,'o',markersize=2,label='regresión por función polinómica')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('IAM')
plt.title("Regresiones de diferentes funciones para el coeficiente de utilización en función del ángulo de incidencia",fontsize=20)
#plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para Martin es:  ' + str(RR_martin)[:str(RR_martin).find(".")+5])
print('El valor del parámetro ar usado es:  ' + str(a_r)[:str(a_r).find(".")+5])
print('El coeficiente de determinación para polinómica es:  ' + str(RR_poli)[:str(RR_poli).find(".")+5])
print('El valor del parametro a1 usado es:  ' + str(a_poli[1])[:str(a_poli[1]).find(".")+5])
print('El valor del parametro a2 usado es:  ' + str(a_poli[2])[:str(a_poli[2]).find(".")+5])
print('El valor del parametro b usado es:  ' + str(b_poli)[:str(b_poli).find(".")+5])


#%%
#-----------------Se calcula el iam con otra normalización

ISC_Nor=(df[(df['aoi']<12)]['ISC_IIIV/DII (A m2/W)'].max())

Valor_normalizar=0.00096
filt_df2['IAM_aoi_']=filt_df2['ISC_IIIV/DII (A m2/W)']/Valor_normalizar


#-------------------datos obtenidos para parametros de funciones de iam-----------------
b=1.1779999732971191
n=0.9000000357627869
k=10.900008201599121
l=0.10000000149011612


#--------------probamos con los parametros obtenidos y con la segunda normalización--------------------------------
y_ashrae=np.array(pvlib.iam.ashrae(aoi=filt_df2['aoi'],b=b))
y_physical=np.array(pvlib.iam.physical(aoi=filt_df2['aoi'], n=n,K=k, L=l))
y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=filt_df2['aoi'],a_r=3140001.0))


RR_physical=E.Determination_coefficient(filt_df2['IAM_aoi_'],y_physical)
RR_ashrae=E.Determination_coefficient(filt_df2['IAM_aoi_'],y_ashrae)
RR_martin=E.regresion_lineal(filt_df2['IAM_aoi_'],y_martin_ruiz)
plt.figure(figsize=(30,15))
plt.plot(filt_df2['aoi'],filt_df2['IAM_aoi_'],'o',markersize=2,label='IAM(AOI)')
plt.plot(filt_df2['aoi'],y_ashrae,'o',markersize=2,label='Ashrae')
plt.plot(filt_df2['aoi'],y_physical,'o',markersize=2,label='Physical')
plt.plot(filt_df2['aoi'],y_martin_ruiz,'o',markersize=2,label='Martin_Ruiz')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('IAM')
plt.title("Diferentes funciones para el IAM en función del ángulo de incidencia con parametros obtenidos",fontsize=20)
#plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para Martin es:  ' + str(RR_martin)[:str(RR_martin).find(".")+5])


#-----------------fitting con los datos de normalizacion de ISC/DII------------


y_ashrae,RR_ashrae,b=IAM_ashrae.regresion_ashrae(filt_df2['aoi'],filt_df2['IAM_aoi_'])
y_physical,RR_physical,n,k,l =IAM_physical_bruto.regresion_physical(filt_df2['aoi'],filt_df2['IAM_aoi_'])
y_martin_ruiz,RR_martin_ruiz,a_r=IAM_Martin.regresion_martin_ruiz(filt_df2['aoi'],filt_df2['IAM_aoi_'])
y_poli,RR_poli,a_poli,b_poli=E.regresion_polinomica(filt_df2['aoi'],filt_df2['IAM_aoi_'],2)

#y_ashrae=np.array(pvlib.iam.ashrae(aoi=filt_df2['aoi'],b=b))
#y_physical=np.array(pvlib.iam.physical(aoi=np.array(filt_df2['aoi']),n=n,K=k,L=l))
#y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=filt_df2['aoi'],a_r=a_r))

plt.figure(figsize=(30,15))
plt.plot(filt_df2['aoi'],filt_df2['IAM_aoi_'],'o',markersize=2,label='todos los datos')
plt.plot(filt_df2['aoi'],y_ashrae,'o',markersize=2,label='Ashrae')
plt.plot(filt_df2['aoi'],y_physical,'o',markersize=2,label='Physical')
plt.plot(filt_df2['aoi'],y_martin_ruiz,'o',markersize=2,label='Martin_Ruiz')
plt.plot(filt_df2['aoi'],y_poli,'o',markersize=2,label='regresión por función polinómica')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('IAM')
plt.title("Diferentes Regresiones para el IAM en función del ángulo de incidencia",fontsize=20)

#    plt.text(12, 0.4,'Temperaturas entre: '+ str(lim_inf)[:str(lim_inf).find(".")]+ 'ºC y '+ str(lim_sup)[:str(lim_sup).find(".")]+'ºC', fontsize=15)
#    plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#    plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#    plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#    plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#    plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#    plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para martin_ruiz es:  ' + str(RR_martin_ruiz)[:str(RR_martin_ruiz).find(".")+5])
print('El valor del parámetro ar usado es: ' + str(a_r))
print('El coeficiente de determinación para polinómica es:  ' + str(RR_poli)[:str(RR_poli).find(".")+5])
print('El valor del parametro a1 usado es:  ' + str(a_poli[1])[:str(a_poli[1]).find(".")+5])
print('El valor del parametro a2 usado es:  ' + str(a_poli[2])[:str(a_poli[2]).find(".")+5])
print('El valor del parametro b usado es:  ' + str(b_poli)[:str(b_poli).find(".")+5])




##--------------------------------------normalizamos la potencia estimada en la base de datos para comparar iams
#P_nor=np.array(df['PMP_estimated_IIIV (W)'])/np.array(df['PMP_estimated_IIIV (W)'].max())
#COS=np.cos(df['aoi']/180*math.pi)
#df['IAM_aoi']=np.array(P_nor/COS)
#filt_df2=df

#
##--------------fitting de potencias con lso parámetros obtenidos------------------------------
#y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
#y_physical=np.array(pvlib.iam.physical(aoi=df['aoi'], n=n,K=k, L=l))
#y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=3140001.0))
#
#RR_physical=E.Determination_coefficient(df['IAM_aoi'],y_physical)
#RR_ashrae=E.Determination_coefficient(df['IAM_aoi'],y_ashrae)
#
#plt.figure(figsize=(30,15))
#plt.plot(df['aoi'],df['IAM_aoi'],'o',markersize=2,label='IAM(AOI)')
#plt.plot(df['aoi'],y_physical,'o',markersize=2,label='funcion_physical')
#plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='ashrae')
#plt.plot(df['aoi'],y_Martin,'o',markersize=2,label='Martin')
#plt.xlabel('Ángulo de incidencia (º)')
#plt.ylabel('Coeficiente de utilización')
#plt.title("Regresiones de diferentes funciones para el coeficiente de utilización en función del ángulo de incidencia",fontsize=20)
##plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
##plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
##plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
##plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
##plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
##plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
#plt.legend()
#plt.show()
#print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
#print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
#print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
#print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
#print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
#print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
##---------------------Se hace el fitting de potencias calculando parámetros que mejor se ajustan---------------
#RR_ashrae,b=IAM_ashrae.regresion_ashrae(df['aoi'],df['IAM_aoi'])
#RR_physical,n,k,l =IAM_physical_bruto.regresion_physical(df['aoi'],df['IAM_aoi'])
#RR_martin_ruiz,a_r=IAM_Martin.regresion_martin_ruiz(df['aoi'],df['IAM_aoi'])
#
#y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
#y_physical=np.array(pvlib.iam.physical(aoi=np.array(df['aoi']),n=n,K=k,L=l))
#y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=a_r))
#
#plt.figure(figsize=(30,15))
#plt.plot(df['aoi'],df['IAM_aoi'],'o',markersize=2,label='todos los datos')
#plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='regresión por ashrae')
#plt.plot(df['aoi'],y_physical,'o',markersize=2,label='regresión por physical')
#plt.plot(df['aoi'],y_martin_ruiz,'o',markersize=2,label='regresión por martin_ruiz')
#plt.xlabel('Ángulo de incidencia (º)')
#plt.ylabel('Factor de utilización IAM')
##    plt.text(12, 0.4,'Temperaturas entre: '+ str(lim_inf)[:str(lim_inf).find(".")]+ 'ºC y '+ str(lim_sup)[:str(lim_sup).find(".")]+'ºC', fontsize=15)
##    plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
##    plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
##    plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
##    plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
##    plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
##    plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
#plt.legend()
#plt.show()
#print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
#print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
#print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
#print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
#print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
#print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
#print('El coeficiente de determinación para martin_ruiz es:  ' + str(RR_martin_ruiz)[:str(RR_martin_ruiz).find(".")+5])
#print('El valor del parámetro ar usado es: ' + str(a_r))
#   

