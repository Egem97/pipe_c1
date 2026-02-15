import pandas as pd
import pytz
import os
from datetime import datetime
from utils.helper import get_months_until_now_from_feb


def read_data_c1_cgroup():
    months = get_months_until_now_from_feb()
    df = pd.DataFrame()
    
    # Obtener la raiz del proyecto de manera robusta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data", "download")

    for month in months:
        #NINOS CARGA
        file_path = os.path.join(data_dir, f"Detalle_nino_{month}.xls")
        try:
            df_ninos = pd.read_excel(file_path, skiprows=7)
            df = df._append(df_ninos, ignore_index=True)
        except FileNotFoundError:
            print(f"⚠️ Archivo no encontrado: {file_path}")
    
    df = df.drop_duplicates()
    DROP_COLS_CVD = [
        'Ubigeo', 'Departamento', 'Provincia', 'Distrito','DNI del Actor Social','Tipo de número telefónico','Tipo Centro Poblado',
        'Centro Poblado','Fecha Mínima de Inicio de Intervención','Fecha Máxima de Intervención','Total de ST Realizados','Total de ST Válidos',
        'Total de ST Válidos WEB','Total de ST Válidos MOVIL',
    ]
    df['Mes'] = df['Fecha Mínima de Inicio de Intervención'].str[5:7]
    df['Año'] = df['Fecha Mínima de Inicio de Intervención'].str[:4]
    df['Mes'] = df['Mes'].astype(int)
    df['Año'] = df['Año'].astype(int)
    df['Celular de la madre'] = df['Celular de la madre'].fillna(0).astype(int)
    df['Motivo referencia'] = df['Motivo referencia'].fillna("Sin Referencia")
    df= df.drop(DROP_COLS_CVD, axis=1)
    df["update"] = datetime.now(pytz.timezone('America/Lima'))
    return df

def read_data_c1_cdetalle():
    months = get_months_until_now_from_feb()
    df = pd.DataFrame()
    
    # Obtener la raiz del proyecto de manera robusta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data", "download")

    for month in months:
        #NINOS CARGA
        file_path = os.path.join(data_dir, f"Reporte_actividades_{month}.xls")
        try:
            df_ninos = pd.read_excel(file_path, skiprows=7)
            df = df._append(df_ninos, ignore_index=True)
        except FileNotFoundError:
            print(f"⚠️ Archivo no encontrado: {file_path}")
    DROP_COLS_AVD = [
        'UBIGEO', 'Departamento', 'Provincia', 'Distrito', 'Codigo EE.SS','Número de Documento AS','Tipo Actor Social',
        'Centro Poblado','Duración (Seg.)','Situación Llamada',
    ]
    df= df.drop(DROP_COLS_AVD, axis=1)
    df['Número de Documento de Niño'] = df['Número de Documento de Niño'].astype(str)
    df['Año'] = df['Año'].astype(str)
    df['Celular de la Madre'] = df['Celular de la Madre'].astype(str)
    df["update"] = datetime.now(pytz.timezone('America/Lima'))
    return df


def read_data_c1_ggroup():
    months = get_months_until_now_from_feb()
    df = pd.DataFrame()
    
    # Obtener la raiz del proyecto de manera robusta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data", "download")

    for month in months:
        #GESTANTES CARGA
        file_path = os.path.join(data_dir, f"Detalle_madre_{month}.xls")
        try:
            df_gestantes = pd.read_excel(file_path, skiprows=7,dtype={"Número de Documento": "str"})
            df_gestantes = df_gestantes.drop_duplicates(subset='Número de Documento', keep='first')
            df = df._append(df_gestantes, ignore_index=True)
            df["Número de Documento"] = df["Número de Documento"].str.strip()
            df['Mes'] = df['Fecha Mínima de Inicio de Intervención'].str[5:7]
            df['Año'] = df['Fecha Mínima de Inicio de Intervención'].str[:4]
        except FileNotFoundError:
            print(f"⚠️ Archivo no encontrado: {file_path}")
    df["update"] = datetime.now(pytz.timezone('America/Lima'))
    return df

def read_data_c1_gdetalle():
    months = get_months_until_now_from_feb()
    df = pd.DataFrame()
    
    # Obtener la raiz del proyecto de manera robusta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data", "download")

    for month in months:
        #GESTANTES CARGA
        file_path = os.path.join(data_dir, f"Reporte_actividades_madres_{month}.xls")
        try:
            df_gestantes = pd.read_excel(file_path,skiprows=7,dtype={"Número de Documento": "str"})
            df = df._append(df_gestantes, ignore_index=True)
            df["Centro Poblado"] = df["Centro Poblado"].replace({False:"OTRO"})
        except FileNotFoundError:
            print(f"⚠️ Archivo no encontrado: {file_path}")
    df["update"] = datetime.now(pytz.timezone('America/Lima'))
    return df




