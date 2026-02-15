import pandas as pd
from job.download_files import download_files_c1
from utils.helper import *
from utils.transform import *
from dotenv import load_dotenv
from utils.ingesta import upload_to_gcs

load_dotenv()
BUCKET = os.getenv("BUCKET_NAME")

def pipeline_data_c1():
    month = month_actual_peru()
    month_text = mes_short(month)
    print(f"Inicio de Download de archivos del mes {month_text}")
    download_files_c1(mes = month_text)
    print(f"Fin de Download de archivos del mes {month_text}")
    print(f"Inicio de Transform de archivos del mes {month_text}")
    df_cgroup = read_data_c1_cgroup()
    df_cdetalle = read_data_c1_cdetalle()
    df_ggroup = read_data_c1_ggroup()
    df_gdetalle = read_data_c1_gdetalle()
    df_cgroup.to_parquet('carga_nino.parquet', engine='pyarrow', index=False)
    df_cdetalle.to_parquet('detalle_nino.parquet', engine='pyarrow', index=False)
    df_ggroup.to_parquet('gestantes.parquet', engine='pyarrow', index=False)
    df_gdetalle.to_parquet('detalle_gestantes.parquet', engine='pyarrow', index=False)
    upload_to_gcs(BUCKET, "carga_nino.parquet", "VISITAS_DOMICILIARIAS_DATA.parquet")
    upload_to_gcs(BUCKET, "detalle_nino.parquet", "DETALLE_VD.parquet")
    upload_to_gcs(BUCKET, "gestantes.parquet", "GESTANTE_VISITAS_DOMICILIARIAS_DATA.parquet")
    upload_to_gcs(BUCKET, "detalle_gestantes.parquet", "GESTANTES_VISITAS_DOMICILIARIAS_DATA.parquet")
    print(f"Fin de Transform de archivos del mes {month_text}")