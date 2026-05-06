from datetime import datetime
import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta

def mestext_short(x):
    dict_mes = {'Ene':1,'Feb':2,'Mar':3,'Abr':4,'May':5,'Jun':6,'Jul':7,'Ago':8,'Set':9,'Oct':10,'Nov':11,'Dic':12}
    return dict_mes[x] 

def mes_short(x):
    """
    Convierte un número de mes a su abreviatura en español.
    """
    dict_mes = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun', 
                7:'Jul', 8:'Ago', 9:'Set', 10:'Oct', 11:'Nov', 12:'Dic'}
    return dict_mes.get(x, str(x))

def month_actual_peru() -> int:
    """
    Obtiene el número del mes actual en la zona horaria de Perú.
    """
    peru_tz = pytz.timezone('America/Lima')
    now_peru = datetime.now(peru_tz)
    return now_peru.month

def get_months_until_now_from_feb():
    """
    Retorna una lista de abreviaturas de meses desde Febrero hasta el mes actual.
    Ejemplo: si es Abril, retorna ['Feb', 'Mar', 'Abr'].
    """
    current_month = month_actual_peru()
    # Si estamos en Enero (1), el rango(2, 2) es vacío, lo cual es correcto si iniciamos en Feb.
    # Si estamos en Febrero (2), range(2, 3) -> [2] -> ['Feb']
    return [mes_short(m) for m in range(2, current_month + 1)]

def remove_duplicate_persons(df):
    """Elimina personas duplicadas manteniendo el registro con nombre más largo"""
    # Crear columna con longitud del nombre
    df['len_nino'] = df['Niño'].str.len()

    # Ordenar por Documento_c1 y por longitud descendente
    df = df.sort_values(['Documento_c1', 'len_nino'], ascending=[True, False])

    # Mantener solo el primer registro por Documento_c1 (el que tiene más caracteres)
    df = df.drop_duplicates(subset=['Documento_c1'], keep='first')

    # Eliminar la columna auxiliar
    df = df.drop(columns=['len_nino']).reset_index(drop=True)

    return df


def childs_unicos_visitados( dataframe = pd.DataFrame, col_name_doc = "", estado = "ALL CHILDS" ):
    
    if estado == "ALL CHILDS":
        vd_ref = dataframe.groupby([col_name_doc,"Etapa"])[["Año"]].count().reset_index()
        vd_ref.columns = ["Documento","Etapa","count"]
        return vd_ref
    elif estado == "CHILDS ETAPA":
        vd_ref = dataframe.groupby([col_name_doc,"Etapa"])[["Año"]].count().reset_index()
        vd_ref.columns = ["Documento","Etapa","count"]
        vd_ref_df = vd_ref.groupby(["Etapa"])[["count"]].count().reset_index()
        vd_ref_df = vd_ref_df.rename(columns=  {"count":"Registros"})
        return vd_ref_df
    elif estado == "ALL CHILDS W DUPLICADOS":
        vd_ref = dataframe.groupby([col_name_doc,"Etapa"])[["Año"]].count().reset_index()
        vd_ref = vd_ref.sort_values(by='Etapa', key=lambda x: x.isin(['No Encontrado', 'Rechazado']))
        vd_ref = vd_ref.drop_duplicates(subset = col_name_doc, keep='first')
        vd_ref.columns = ["Documento","Etapa","count"]
        return vd_ref
    elif estado == "CHILDS ETAPA W DUPLICADOS":
        vd_ref = dataframe.groupby([col_name_doc,"Etapa"])[["Año"]].count().reset_index()
        vd_ref = vd_ref.sort_values(by='Etapa', key=lambda x: x.isin(['No Encontrado', 'Rechazado']))
        vd_ref = vd_ref.drop_duplicates(subset = col_name_doc, keep='first')
        vd_ref.columns = ["Documento","Etapa","count"]
        vd_ref_df = vd_ref.groupby(["Etapa"])[["count"]].count().reset_index()
        vd_ref_df = vd_ref_df.rename(columns=  {"count":"Registros"})
        return vd_ref_df

def estado_visitas_completas(x,y,estado):
    if estado == "No Encontrado" or estado == "Rechazado":
        return f"Visita Niño:{estado}"
    else:

        if x == y:
            return "Visitas Completas"
        elif x > y:
            res = x-y
            return f"Visitas Incompletas(faltantes:{res})"
        elif y > x:
            return "Visitas Completas (exedido)"
def calcular_edad(fecha_nacimiento):
    hoy = pd.to_datetime('today')
    diferencia = relativedelta(hoy, fecha_nacimiento)
    return f"{diferencia.years} año(s), {diferencia.months} mes(es)"


def combinar_rangos_dias(row):
            rangos_activos = []
            if row['Niños 120-149 días en mes'] == 'SI':
                rangos_activos.append('Rango de días 120-149 días')
            if row['Niños 180-209 días en mes'] == 'SI':
                rangos_activos.append('Rango de días 180-209 días')
            if row['Niños 270-299 días en mes'] == 'SI':
                rangos_activos.append('Rango de días 270-299 días')
            if row['Niños 360-389 días en mes'] == 'SI':
                rangos_activos.append('Rango de días 360-389 días')
            
            if rangos_activos:
                return ' | '.join(rangos_activos)
            else:
                return 'Sin rango específico'

def calcular_fecha_cumple(row):
                    rango = row['Rango de Días Activo']
                    fecha_nac = row['Fecha de Nacimiento']
                    
                    if rango == "Rango de días 120-149 días":
                        return fecha_nac + pd.Timedelta(days=120)
                    elif rango == "Rango de días 180-209 días":
                        return fecha_nac + pd.Timedelta(days=180)
                    elif rango == "Rango de días 270-299 días":
                        return fecha_nac + pd.Timedelta(days=270)
                    elif rango == "Rango de días 360-389 días":
                        return fecha_nac + pd.Timedelta(days=360)
                    else:
                        return pd.NaT  # Para casos sin rango específico