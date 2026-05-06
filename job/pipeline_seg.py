import pandas as pd
import os
import json
from job.download_files import download_files_c1
from utils.load_parquet import *
from utils.helper import *
from utils.g_sheet import *
from utils.ingesta import upload_to_gcs


def pipeline_seg():
    load_dotenv()
    BUCKET = os.getenv("BUCKET_NAME")
    seg_nominal = os.getenv("SEG_NOM")
    seg_nominal = json.loads(seg_nominal)
    dataframe_general = pd.DataFrame()
    for mes, sheet in seg_nominal.items():
        df =read_and_concatenate_sheets_optimized(
                            
                            key_sheet=sheet,
                            sheet_names=[
                            "ARANJUEZ","CLUB DE LEONES","EL BOSQUE",'LOS GRANADOS "SAGRADO CORAZON"',
                            "CENTRO DE SALUD LA UNION","HOSPITAL DE ESPECIALIDADES BASI",
                            "LIBERTAD","LOS JARDINES","PESQUEDA III","SAN MARTIN DE PORRES"
                        ],
                        add_sheet_column=True  # Añade columna 'sheet_origen'
                    )
        df["Mes"] = mes
        dataframe_general = pd.concat([dataframe_general, df], ignore_index=True)
    dataframe_general = dataframe_general[(dataframe_general["Número de Documento del niño"] != "") & (dataframe_general["Establecimiento de Salud"] != "")]
    
    dataframe_general = dataframe_general[[
        'Mes','Número de Documento del niño','FUE PARTE DE SESION DE MOSTRATIVA?','Fecha de la sesion demostrativa','Edad',
        'Fecha HISEADO (Sesión Demostrativa)','TIPO DE SEGURO','¿Es prematuro?','Fecha del tamizaje de Hemoglobina de 06 MESES','Resultado de Hemoglobina de 06 MESES',
        'Tipo de Suplemento', 'Fecha del tamizaje de Hemoglobina de 09 MESES','Resultado de Hemoglobina de 09 MESES','Fecha del tamizaje de Hemoglobina de 12 MESES',
       'Resultado de Hemoglobina de 12 MESES'
    ]]
    
    # Convertir a datetime temporalmente para extraer datos y estandarizar
    fechas_dt = pd.to_datetime(
        dataframe_general['Fecha de la sesion demostrativa'], 
        errors='coerce', 
        dayfirst=True
    )
    
    # Crear la nueva columna MES_SD extrayendo el mes (1 al 12)
    dataframe_general['MES_SD'] = fechas_dt.dt.month
    dataframe_general['MES_SD'] = dataframe_general['MES_SD'].apply(lambda x: mes_short(x))
    dataframe_general['MES_SD'] = dataframe_general['MES_SD'].replace("nan",None)
    # Estandarizar la columna de fechas original
    dataframe_general['Fecha de la sesion demostrativa'] = fechas_dt.dt.strftime('%d/%m/%Y')
    dataframe_general = dataframe_general.rename(columns={
        "Edad":"Edad_create_sd","Número de Documento del niño":"Número de Documento"
    })
    dataframe_general["Mes"] = dataframe_general["Mes"].apply(lambda x: mes_short(x))
    dataframe_general.to_parquet("./data/base/SEGUIMIENTO_NOMINAL_.parquet")
    upload_to_gcs(BUCKET, "./data/base/SEGUIMIENTO_NOMINAL_.parquet", "SEGUIMIENTO_NOMINAL_.parquet")