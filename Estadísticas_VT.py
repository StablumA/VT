import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import geopandas as gpd
import folium
from folium import plugins
df = pd.read_csv("10-TX-SData.csv",sep=',',parse_dates=['Fecha Hora'],dayfirst=True)
df['Fecha Hora']=pd.to_datetime(df['Fecha Hora'])

# elimino primer columna
df=df.drop(df.columns[[0]],axis=1)

# filtro por tipo de día
df['Dia']=df['Fecha Hora'].dt.day
df['nDia']=df['Fecha Hora'].dt.day_name()
#saco los sabados y domingos
dfhabil= df[df['nDia'].isin(['Monday','Tuesday','Wednesday','Thursday','Friday'])]
# saco los feriados
feriados = [7,10]
dfhabil= dfhabil[dfhabil['Dia']!= (i for i in feriados)]

print(dfhabil)
## Veo num. de transacciones por  'Linea' en el total de días habiles
TxL= dfhabil.groupby(['Ramal']).size().to_frame('NTrans')
Thabiles= len(dfhabil['Dia'].unique())
print(TxL)
# obtengo el promedio por día x linea
PromedioHabiles= TxL.apply(lambda NTrans: (NTrans/Thabiles), axis=1)
PromedioHabiles= PromedioHabiles.astype({"NTrans":"int"})
print(PromedioHabiles)

total = PromedioHabiles["NTrans"].sum()
factor = 100/total

PromedioHabiles['FracUso']= PromedioHabiles['NTrans'].apply(lambda cant: (cant*factor))
PromedioHabiles=PromedioHabiles.sort_values(by ="FracUso", ascending=False)
print(PromedioHabiles)

## realizo un gráfico
fig, ax 
