import re
import pandas as pd
import gspread
import time
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
load_dotenv()
# Paso 1: Autenticación
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GESTOR_FILE"), scope)
client = gspread.authorize(creds)

def _sanitize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y desduplica nombres de columnas para evitar errores de reindex.
    - Quita espacios
    - Reemplaza vacíos por 'Col_i'
    - Desduplica añadiendo sufijos _2, _3, ...
    """
    cols = [str(c).strip() if (c is not None) else '' for c in df.columns]
    cols = [c if c != '' else f'Col_{i+1}' for i, c in enumerate(cols)]
    s = pd.Series(cols)
    s = s.where(~s.duplicated(), s + '_' + (s.groupby(s).cumcount() + 1).astype(str))
    df.columns = s
    return df

def read_and_concatenate_sheets_optimized(key_sheet, sheet_names, add_sheet_column=True):
    """
    Versión optimizada que abre el spreadsheet una sola vez y lee todas las hojas.
    Mucho más eficiente para múltiples hojas.
    
    Args:
        key_sheet (str): ID de la hoja de Google Sheets
        sheet_names (list): Lista con los nombres de las hojas a leer
        add_sheet_column (bool): Si True, añade una columna con el nombre de la hoja de origen
    
    Returns:
        pandas.DataFrame: DataFrame concatenado con todos los datos o None si hay error
    """
    all_dataframes = []
    successful_sheets = []
    failed_sheets = []
    
    
    spreadsheet = client.open_by_key(key_sheet)
        
        # Obtener información de todas las hojas disponibles
    available_sheets = {ws.title: ws for ws in spreadsheet.worksheets()}
        
       

    for sheet_name in sheet_names:
                try:
                    # Verificar si la hoja existe
                    if sheet_name not in available_sheets:
                        failed_sheets.append(f"{sheet_name}: Hoja no encontrada")
                        continue
                    
                    # Obtener datos de la hoja
                    worksheet = available_sheets[sheet_name]
                    data = worksheet.get_all_values()
                   # st.write(sheet_name)
                    #st.write(data)
                    # Convertir a DataFrame si hay datos
                    if data and len(data) > 0:
                        #st.write(data)
                        # Usar la primera fila como headers
                        if len(data) > 1:
                            df = pd.DataFrame(data[1:], columns=data[0])
                            
                        else:
                            df = pd.DataFrame(data)
                        #st.write(df.shape)
                        # Limpiar DataFrame (eliminar filas completamente vacías)
                        df = df.dropna(how='all')
                        
                        if not df.empty:
                            # Normalizar/Desduplicar columnas
                            df = _sanitize_columns(df)
                            # Añadir columna con el nombre de la hoja si se solicita
                            if add_sheet_column:
                                df['sheet_origen'] = sheet_name
                            df = df.reset_index(drop=True)
                            all_dataframes.append(df)
                            successful_sheets.append(sheet_name)
                        else:
                            failed_sheets.append(f"{sheet_name}: Hoja vacía después de limpiar")
                    else:
                        failed_sheets.append(f"{sheet_name}: Sin datos")
                        
                except Exception as e:
                    failed_sheets.append(f"{sheet_name}: {str(e)}")
                    continue
        
        
        # Concatenar DataFrames si hay datos
       
        #st.write(all_dataframes)

        
    
    concatenated_df = pd.concat(all_dataframes, ignore_index=True)
    return concatenated_df


            