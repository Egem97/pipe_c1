from datetime import datetime
import pytz

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
