import pandas as pd
from google.cloud import storage
from dotenv import load_dotenv
from urllib.parse import quote
import os
load_dotenv()
CS_URL = os.getenv('CS_URL')

def get_vd_childs():return pd.read_parquet(f'https://{CS_URL}/DETALLE_VD.parquet', engine='pyarrow')

def get_carga_childs(): return pd.read_parquet(f'https://{CS_URL}/VISITAS_DOMICILIARIAS_DATA.parquet', engine='pyarrow')

def get_vd_gestantes():return pd.read_parquet(f'https://{CS_URL}/GESTANTES_VISITAS_DOMICILIARIAS_DATA.parquet', engine='pyarrow')#

def get_carga_gestantes():return pd.read_parquet(f'https://{CS_URL}/GESTANTE_VISITAS_DOMICILIARIAS_DATA.parquet', engine='pyarrow')
    
def get_data_gestantes():return pd.read_parquet(f'https://{CS_URL}/datos_gestantes.parquet', engine='pyarrow')

def get_data_childs():return pd.read_parquet(f'https://{CS_URL}/{quote("datos_niños.parquet")}', engine='pyarrow')



def get_padron():return pd.read_parquet(f'https://{CS_URL}/PADRON_TRUJILLO.parquet', engine='pyarrow')

def get_sd():return pd.read_parquet(f'https://{CS_URL}/SEGUIMIENTO_NOMINAL_.parquet', engine='pyarrow')











