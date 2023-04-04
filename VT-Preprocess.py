import pandas as pd
import numpy as np
#### importo los datos
Ts_oct= pd.read_csv("10 Transacciones Octubre 2022.csv", sep= ';', parse_dates=["Fecha Hora"], dayfirst=True)
Ts_oct= Ts_oct[Ts_oct["Fecha Hora"]>= pd.to_datetime('1-10-2022', format='%d-%m-%Y')]
df=Ts_oct

df["MES"]= df["Fecha Hora"].dt.month
df= df[df["MES"]== 10]

## filtro los duplicados
bool_series= df.duplicated(keep='first')
df= df[~bool_series]

# borro la primer columna
df = df.drop(df.columns[0],axis=1)
da = df

### saco el ! a las líneas
def limp(numer):
    auxiliar=str(numer["Linea"])[1:]
    return auxiliar
df['LINEA']=df.apply(lambda row: limp(row), axis=1)

da = df
# me llevo lo que no se repite
df= df[["Interno","LINEA","Ramal","Tipo Trx","Fecha Hora","Hora","Tarifa Marcada","Tarifa Cobrada","Tarjeta","Legajo","Latitud","Longitud"]]
df= df.rename(columns={"LINEA":"Linea"})
da.to_csv("VT_OCT.csv")
df.to_csv("10-TX-SData.csv")

