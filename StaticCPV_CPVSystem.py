# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:56:02 2020

@author: juanjo
"""
from pvlib.location import Location
import CPVClass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Error as E
import datetime
import pvlib
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
tz='Europe/Berlin'
#AOILIMIT
AOILIMIT=55.0

#Se construye el objeto CPVSystem
Mi_CPV=CPVClass.CPVSystem(surface_tilt=30, surface_azimuth=180,
                 albedo=None, surface_type=None,
                 module=None, 
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 losses_parameters=None, name=None,
                 iam_parameters=None)


Mi_CPV.module_CPV_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.0004, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9, 'pdc0': 25,'gamma_pdc':-0.005 }


Mi_CPV.temperature_model_CPV_parameters={'u_c': 9,'u_v':0}

Mi_CPV.iam_CPV_parameters={'a3':-8.315977512579876e-06,'a2': 0.00039212250547851317,
                        'a1':-0.006006260890940136,'valor_norm':0.0008882140968826235}

# Mi_CPV.uf_parameters={'m1_am':0.172793, 'thld_am':1.285187 ,'m2_am':-0.408000,
#                       'm_temp':-0.006439, 'thld_temp':15.18,
#                        'w_am':0.41400000000000003,'w_temp': 0.464}

# Mi_CPV.uf_parameters={'m1_am':0.173885, 'thld_am':1.285187 ,'m2_am':-0.410000,
#                       'm_temp':-0.006480, 'thld_temp':15.180000,
#                         'w_am':0.369,'w_temp': 0.623}
Mi_CPV.uf_parameters={'m1_am':-0.1448392843942126, 'thld_am':1.2432864275564657 ,'m2_am':-0.7409999999999998,
                      'm_temp':-0.006480, 'thld_temp':15.180000,
                        'w_am':0,'w_temp': 0.0}


#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
Mi_CPV.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}

#LOCALIZED SYSTEM
#Datos:
#localizaci??n
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'

CPV_location=Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
localized_Mi_CPV=CPVClass.LocalizedCPVSystem(cpvsystem=Mi_CPV,second_object=CPV_location)

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

#SE filtran los datos que no correspondan a una tendencia clara de la potencia.
CPV=df[(df['aoi']<=AOILIMIT)]
Fecha=pd.DatetimeIndex(CPV['Date Time'])
CPV=CPV.set_index(Fecha)
CPV=CPV.drop(['Date Time'],axis=1)
CPV_=CPV
#Se limpian un poco los datos de potencia por medio de la mediana 
CPV=E.mediana_filter(CPV,'aoi','PMP_estimated_IIIV (W)',200,15)

plt.figure(figsize=(30,15))
plt.plot(CPV_['aoi'],CPV_['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos filtrados con mediana')
plt.xlabel('??ngulo de incidencia (??)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Visualizar los datos filtrados por la mediana')
plt.legend()

CPV=E.mediana_filter(data=CPV,colum_intervals='aoi',columna_filter='DII (W/m2)',n_intervalos=20,porcent_mediana=10)
CPV['DII_efectiva (W/m2)']=CPV['DII (W/m2)']*Mi_CPV.get_CPV_iam(CPV['aoi'],iam_model='third degree')

fig=plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['DII_efectiva (W/m2)'],'o',markersize=4,label='DII con iam')   
plt.plot(CPV['aoi'],CPV['DII (W/m2)'],'o',markersize=4,label='DII')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('??ngulo de incidencia (??)',fontsize=30)
plt.ylabel('Irradiancia (W/m2)',fontsize=30)
plt.legend(fontsize=30,markerscale=3)
plt.title("Comparaci??n de la irradiancia corregida",fontsize=40)

# C??lculo de la temperatura de cell
temp_cell=Mi_CPV.CPV_temp(poa_global=CPV['DII_efectiva (W/m2)'], temp_air=CPV['T_Amb (??C)'], wind_speed=CPV['Wind Speed (m/s)']) 
# temp_cell=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII_efectiva (W/m2)'], 
#                                         temp_air=CPV['T_Amb (??C)'],
#                                         wind_speed=CPV['Wind Speed (m/s)'], 
#                                         u_c=4.5, u_v=0.0, 
#                                         eta_m=0.32, alpha_absorption=0.9)
temp_cell_=Mi_CPV.CPV_temp(poa_global=CPV['DII (W/m2)'], temp_air=CPV['T_Amb (??C)'], wind_speed=CPV['Wind Speed (m/s)'])
 
fig=plt.figure(figsize=(30,15))
plt.plot(CPV.index[:].time,temp_cell,'o',markersize=2,label='Temperatura con DII corregida')   
plt.plot(CPV.index[:].time,temp_cell_,'o',markersize=2,label='Temperatura con DII')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Horas',fontsize=30)
plt.ylabel('Temperatura de c??lula (??C)',fontsize=30)
plt.legend(fontsize=30,markerscale=3)
plt.title("Temperatura de c??lula a lo largo de las horas de un d??a ",fontsize=40)

#%%
Five_parameters=Mi_CPV.CPV_calcparams(CPV['DII_efectiva (W/m2)'], temp_cell)
Five_parameters_=Mi_CPV.CPV_calcparams(CPV['DII (W/m2)'], temp_cell_)

Curvas=Mi_CPV.CPV_singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=Mi_CPV.CPV_singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')

UF=Mi_CPV.calculate_uf(CPV['airmass_relative'].values,CPV['T_Amb (??C)'].values,
             Curvas['p_mp'],CPV['PMP_estimated_IIIV (W)'].values)

# Potencia=Curvas['p_mp']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (??C)'].values)
Potencia=Curvas['p_mp']*UF
Diferencia_potencia=Potencia-CPV['PMP_estimated_IIIV (W)'].values
Diferencia_potencia_=Curvas['p_mp']-CPV['PMP_estimated_IIIV (W)'].values
Diferencia_potencia_dat=Curvas_['p_mp']-CPV['PMP_estimated_IIIV (W)'].values

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos')
plt.plot(CPV['aoi'],Curvas_['p_mp'],'o',markersize=2,label='Sin corregir')
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['aoi'],Potencia,'o',markersize=2,label='Corregido con IAM y UF')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('??ngulo de incidencia (??)',fontsize=30)
plt.ylabel('Potencia (W)',fontsize=30)
plt.title('Previsi??n de potencia',fontsize=40)
plt.legend(fontsize=30,markerscale=3)


Datos_max=CPV['PMP_estimated_IIIV (W)'].max()
Datos_min=CPV['PMP_estimated_IIIV (W)'].min()
Datos_media=sum(CPV['PMP_estimated_IIIV (W)'].values)/len(CPV['PMP_estimated_IIIV (W)'].values)
RMSE_potencia=E.RMSE(CPV['PMP_estimated_IIIV (W)'],Potencia)
MAE_potencia=E.MAE(CPV['PMP_estimated_IIIV (W)'], Potencia)
Potencia_max=Potencia.max()
Potencia_min=Potencia.min()
Potencia_media=sum(Potencia)/len(Potencia)
RMSE_potencia_iam=E.RMSE(CPV['PMP_estimated_IIIV (W)'],Curvas['p_mp'])
MAE_potencia_iam=E.MAE(CPV['PMP_estimated_IIIV (W)'], Curvas['p_mp'])
Potencia_iam_max=Curvas['p_mp'].max()
Potencia_iam_min=Curvas['p_mp'].min()
Potencia_iam_media=sum(Curvas['p_mp'])/len(Curvas['p_mp'])
RMSE_potencia_nada=E.RMSE(CPV['PMP_estimated_IIIV (W)'],Curvas_['p_mp'])
MAE_potencia_nada=E.MAE(CPV['PMP_estimated_IIIV (W)'], Curvas_['p_mp'])
Potencia_max_nada=Curvas_['p_mp'].max()
Potencia_min_nada=Curvas_['p_mp'].min()
Potencia_medi_nada=sum(Curvas_['p_mp'])/len(Curvas_['p_mp'])

print("Estos son los resultados obtenidos para la potencia:")
print("Datos")
print("Potencia m??xima: ", Datos_max)
print("Potencia m??nima: ", Datos_min)
print("Potencia media: ", Datos_media)
print("Aplicando IAM y UF")
print("Potencia m??xima: ", Potencia_max)
print("Potencia m??nima: ", Potencia_min)
print("Potencia media: ", Potencia_media)
print("RMSE potencia: ", RMSE_potencia)
print("MAE potencia: ", MAE_potencia)
print("Aplicando IAM")
print("Potencia m??xima: ", Potencia_iam_max)
print("Potencia m??nima: ", Potencia_iam_min)
print("Potencia media: ", Potencia_iam_media)
print("RMSE potencia: ", RMSE_potencia_iam)
print("MAE potencia: ", MAE_potencia_iam)
print("Si aplicar modelos de correcci??n")
print("Potencia m??xima: ", Potencia_max_nada)
print("Potencia m??nima: ", Potencia_min_nada)
print("Potencia media: ", Potencia_iam_media)
print("RMSE potencia: ", RMSE_potencia_nada)
print("MAE potencia: ", MAE_potencia_nada)


plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Diferencia_potencia,'o',markersize=2,label='Corregido con IAM y UF')
plt.plot(CPV['aoi'],Diferencia_potencia_,'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['aoi'],Diferencia_potencia_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('??ngulo de incidencia (??)',fontsize=30)
plt.ylabel('Error de potencia (W)',fontsize=30)
plt.title('Residuos en funci??n del ??ngulo de incidencia',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_relative'],Diferencia_potencia,'o',markersize=2,label='Corregido con IAM y UF')
plt.plot(CPV['airmass_relative'],Diferencia_potencia_,'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['airmass_relative'],Diferencia_potencia_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Masa del aire (n.d.)',fontsize=30)
plt.ylabel('Error de potencia (W)',fontsize=30)
plt.title('Residuos en funci??n de la masa del aire',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (??C)'],Diferencia_potencia,'o',markersize=2,label='Corregido con IAM y UF')
plt.plot(CPV['T_Amb (??C)'],Diferencia_potencia_,'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['T_Amb (??C)'],Diferencia_potencia_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (??C)',fontsize=30)
plt.ylabel('Error de potencia (W)',fontsize=30)
plt.title('Residuos en funci??n de la temperatura',fontsize=40)
plt.legend(fontsize=30,markerscale=3)


#ahora se comprueba la intensidad
Intensidad=Curvas['i_sc']*UF
Diferencia_intensidad=Intensidad-CPV['ISC_measured_IIIV (A)'].values
Diferencia_intensidad_=Curvas['i_sc']-CPV['ISC_measured_IIIV (A)'].values
Diferencia_intensidad_dat=Curvas_['i_sc']-CPV['ISC_measured_IIIV (A)'].values

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['ISC_measured_IIIV (A)'],'o',markersize=2,label='Datos')
plt.plot(CPV['aoi'],Curvas_['i_sc'],'o',markersize=2,label='Sin corregir')
plt.plot(CPV['aoi'],Curvas['i_sc'],'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['aoi'],Intensidad,'o',markersize=2,label='Corregido con IAM y UF')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('??ngulo de incidencia (??)',fontsize=30)
plt.ylabel('Intensidad de cortocircuito (A)',fontsize=30)
plt.title('Previsi??n de intensidad',fontsize=40)
plt.legend(fontsize=30,markerscale=3)


Datos_i_max=CPV['ISC_measured_IIIV (A)'].max()
Datos_i_min=CPV['ISC_measured_IIIV (A)'].min()
Datos_i_media=sum(CPV['ISC_measured_IIIV (A)'].values)/len(CPV['ISC_measured_IIIV (A)'].values)
RMSE_intensidad=E.RMSE(CPV['ISC_measured_IIIV (A)'],Intensidad)
MAE_intensidad=E.MAE(CPV['ISC_measured_IIIV (A)'], Intensidad)
intensidad_max=Intensidad.max()
intensidad_min=Intensidad.min()
intensidad_media=sum(Intensidad)/len(Intensidad)
RMSE_intensidad_iam=E.RMSE(CPV['ISC_measured_IIIV (A)'],Curvas['i_sc'])
MAE_intensidad_iam=E.MAE(CPV['ISC_measured_IIIV (A)'], Curvas['i_sc'])
intensidad_iam_max=Curvas['i_sc'].max()
intensidad_iam_min=Curvas['i_sc'].min()
intensidad_iam_media=sum(Curvas['i_sc'])/len(Curvas['i_sc'])
RMSE_intensidad_nada=E.RMSE(CPV['ISC_measured_IIIV (A)'],Curvas_['i_sc'])
MAE_intensidad_nada=E.MAE(CPV['ISC_measured_IIIV (A)'], Curvas_['i_sc'])
intensidad_max_nada=Curvas_['i_sc'].max()
intensidad_min_nada=Curvas_['i_sc'].min()
intensidad_medi_nada=sum(Curvas_['i_sc'])/len(Curvas_['i_sc'])

print("Estos son los resultados obtenidos para la intensidad:")
print("Datos")
print("Intensidad m??xima: ", Datos_i_max)
print("Intensidad m??nima: ", Datos_i_min)
print("Intensidad media: ", Datos_i_media)
print("Aplicando IAM y UF")
print("Intensidad m??xima: ", intensidad_max)
print("Intensidad m??nima: ", intensidad_min)
print("Intensidad media: ", intensidad_media)
print("RMSE Intensidad: ", RMSE_intensidad)
print("MAE Intensidad: ", MAE_intensidad)
print("Aplicando IAM")
print("Intensidad m??xima: ", intensidad_iam_max)
print("Intensidad m??nima: ", intensidad_iam_min)
print("Intensidad media: ", intensidad_iam_media)
print("RMSE Intensidad: ", RMSE_intensidad_iam)
print("MAE Intensidad: ", MAE_intensidad_iam)
print("Si aplicar modelos de correcci??n")
print("Intensidad m??xima: ", intensidad_max_nada)
print("Intensidad m??nima: ", intensidad_min_nada)
print("Intensidad media: ", intensidad_medi_nada)
print("RMSE Intensidad: ", RMSE_intensidad_nada)
print("MAE Intensidad: ", MAE_intensidad_nada)



plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Diferencia_intensidad,'o',markersize=2,label='Corregido con IAM y UF')
plt.plot(CPV['aoi'],Diferencia_intensidad_,'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['aoi'],Diferencia_intensidad_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('??ngulo de incidencia (??)',fontsize=30)
plt.ylabel('Error de intensidad (A)',fontsize=30)
plt.title('Residuos en funci??n del ??ngulo de incidencia',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_relative'],Diferencia_intensidad,'o',markersize=2,label='Corregido con IAM y UF')
plt.plot(CPV['airmass_relative'],Diferencia_intensidad_,'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['airmass_relative'],Diferencia_intensidad_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Masa del aire (n.d.)',fontsize=30)
plt.ylabel('Error de intensidad (A)',fontsize=30)
plt.title('Residuos en funci??n de la masa del aire',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (??C)'],Diferencia_intensidad,'o',markersize=2,label='Corregido con IAM y UF')
plt.plot(CPV['T_Amb (??C)'],Diferencia_intensidad_,'o',markersize=2,label='Corregido con IAM')
plt.plot(CPV['T_Amb (??C)'],Diferencia_intensidad_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (??C)',fontsize=30)
plt.ylabel('Error de intensidad (A)',fontsize=30)
plt.title('Residuos en funci??n de la temperatura',fontsize=40)
plt.legend(fontsize=30,markerscale=3)







#%% Se ha observado que por medio del procedimiento se obtienen un errror dependiente del aoi y del airmass

'''
Data_iam=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx',sheet_name='C??lculo_iam_CPV',encoding='utf-8')
Data_am=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx',sheet_name='C??lculo_uf_am_CPV',encoding='utf-8')
Data_temp=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx',sheet_name='C??lculo_uf_temp_CPV',encoding='utf-8')

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

#SE filtran los datos que no correspondan a una tendencia clara de la potencia.
CPV=df[(df['aoi']<=AOILIMIT)]
Fecha=pd.DatetimeIndex(CPV['Date Time'])
CPV=CPV.set_index(Fecha)
CPV=CPV.drop(['Date Time'],axis=1)
CPV_=CPV 
CPV=E.mediana_filter(CPV,'aoi','PMP_estimated_IIIV (W)',200,15)
CPV=E.mediana_filter(data=CPV,colum_intervals='aoi',columna_filter='DII (W/m2)',n_intervalos=20,porcent_mediana=10)


#Se construye el objeto CPVSystem
Mi_CPV=CPVClass.CPVSystem(surface_tilt=30, surface_azimuth=180,
                 AOILIMIT=55.0,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)



Mi_CPV.generate_iam_parameters(Data_iam['aoi'].values, Data_iam['ISC_IIIV/DII (A m2/W)'].values,grado=2)



#%%
Mi_CPV.generate_uf_am_parameters(Data_iam['airmass_relative'].values, Data_iam['ISC_IIIV/DII (A m2/W)'].values,grado=2)


CPV['DII_efectiva (W/m2)']=CPV['DII (W/m2)']*Mi_CPV.get_iam(CPV['aoi'],iam_model='third degree')

temp_cell=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII_efectiva (W/m2)'], temp_air=CPV['T_Amb (??C)'], wind_speed=CPV['Wind Speed (m/s)']) 
temp_cell_=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII (W/m2)'], temp_air=CPV['T_Amb (??C)'], wind_speed=CPV['Wind Speed (m/s)'])

Five_parameters=Mi_CPV.calcparams_cpvsyst(CPV['DII_efectiva (W/m2)'], temp_cell)
Five_parameters_=Mi_CPV.calcparams_cpvsyst(CPV['DII (W/m2)'], temp_cell_)

Curvas=Mi_CPV.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=Mi_CPV.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')

# Mi_CPV.generate_uf_temp_parameters(Data_temp['T_Amb (??C)'].values, Data_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values)

# Mi_CPV.generate_uf_am_parameters(Data_am['airmass'].values, Data_am['ISC_IIIV/DII_efectiva (A m2/W)'].values)
#%%
# Mi_CPV.generate_uf_am_parameters2(Data_am['airmass'].values, Data_am['ISC_IIIV/DII_efectiva (A m2/W)'].values)


#%%


# Mi_CPV.uf_parameters['w_am']=0
# Mi_CPV.uf_parameters['w_temp']=0



# Mi_CPV.calculate_UF(CPV['airmass_relative'].values, CPV['T_Amb (??C)'].values, Curvas['p_mp'], CPV['PMP_estimated_IIIV (W)'].values)


#%% YA QUE HAY DOS METODOS PARA EL UF_AM HAY QUE COMPARARLOS NO SOLO CON EL RMSE



Mi_CPV.uf_parameters={'m1_am':0.172793, 'thld_am':1.285187 ,'m2_am':-0.408000,
                      'm_temp':-0.006439, 'thld_temp':15.18,
                      'w_am':0.422,'w_temp': 0.492}

Potencia_1=Curvas['p_mp']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (??C)'].values)
Diferencia_1=Potencia_1-CPV['PMP_estimated_IIIV (W)'].values
RMSE_1=E.RMSE(CPV['PMP_estimated_IIIV (W)'].values,Potencia_1)

Intensidad_1=Curvas['i_sc']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (??C)'].values)


Mi_CPV.uf_parameters={'m1_am': 0.18645008054738124,
                      'thld_am': 1.3081866727630114,
                      'm2_am': -0.32677187580032385,
                      'm_temp': -0.006439,
                      'thld_temp': 15.18,
                      'w_am': 0.161,
                      'w_temp': 0.765}

Potencia_2=Curvas['p_mp']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (??C)'].values)
Diferencia_2=Potencia_2-CPV['PMP_estimated_IIIV (W)'].values
RMSE_2=E.RMSE(CPV['PMP_estimated_IIIV (W)'].values,Potencia_2)
Intensidad_2=Curvas['i_sc']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (??C)'].values)

#%%

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencia_1,'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('??ngulo de incidencia (??)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparaci??n de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Diferencia_1,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('??ngulo de incidencia (??)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (??C)'],Diferencia_1,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (??C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_relative'],Diferencia_1,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencia_2,'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('??ngulo de incidencia (??)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparaci??n de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Diferencia_2,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('??ngulo de incidencia (??)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (??C)'],Diferencia_2,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (??C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_relative'],Diferencia_2,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


'''




# Hola=localized_Mi_CPV.get_iam(CPV['aoi'],iam_model='third degree')

# # Hola=localized_Mi_CPV.get_aoi(solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'])






