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
PromedioHabiles= dfhabil.groupby(['Ramal']).size().to_frame('NTrans').reset_index()
Thabiles= len(dfhabil['Dia'].unique())
# obtengo el promedio por día x linea

PromedioHabiles['NTransPromedio']= PromedioHabiles['NTrans'].apply(lambda NTrans: (NTrans/Thabiles))
#PromedioHabiles= PromedioHabiles.astype({"NTrans":"int"})
print(PromedioHabiles)

total = PromedioHabiles["NTransPromedio"].sum()
factor = 100/total

PromedioHabiles['FracUso']= PromedioHabiles["NTransPromedio"].apply(lambda cant: (cant*factor))
PromedioHabiles= PromedioHabiles.astype({'FracUso':'int'})
PromedioHabiles=PromedioHabiles.sort_values(by ="NTransPromedio", ascending=False)
print(PromedioHabiles)

## realizo un gráfico
fig, ax = plt.subplots(figsize=(8,4))
ax.barh(PromedioHabiles['Ramal'].astype('str'), PromedioHabiles["NTrans"], color=["#12bc8e"])

for c in ax.containers:
    labels = [(renglon for v in PromedioHabiles['FracUso'])]
    ax.bar_label(c, labels=labels,label_type='edge',padding=0.3)
ax.xaxis.set_tick_params(pad=5)
ax.yaxis.set_tick_params(pad=5) # dist de las etiquetas
ax.grid(color='green',linestyle='-.',linewidth=0.5,alpha=0.15)
ax.invert_yaxis()
ax.set_title(" Barplot de las transacciones promedio en un día hábil, por línea",
             loc='center', fontname='Arial',fontsize='10', pad=5,color='black')
plt.suptitle("Transacciones promedio por línea",
              fontname='Arial',fontsize='20',color='black', fontweight='bold',y=0.99)
plt.show()
