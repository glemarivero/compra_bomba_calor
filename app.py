import streamlit as st
import pandas as pd
import numpy as np
from utils import get_costo_hora, get_precio_fuel_oil, get_config, get_usd_uyu_conversion

st.set_page_config(layout="wide")


DEFAULT_MESES = 3
DEFAULT_HORAS = [22, 23, 0, 5, 6, 7, 15, 16, 17]
USD = float(st.sidebar.text_input('Dolar', value=get_usd_uyu_conversion()))
COSTO_FUEL_OIL = float(st.sidebar.text_input('Costo L fuel oil', value=str(get_precio_fuel_oil())))
CONSUMO_ANUAL_FUEL_OIL = float(st.sidebar.text_input('Consumo anual fuel oil (L)', value='12000'))
COSTO_ANUAL_CALDERA_USD = COSTO_FUEL_OIL * CONSUMO_ANUAL_FUEL_OIL / USD
st.sidebar.write(f'Costo anual fuel oil (USD): {COSTO_ANUAL_CALDERA_USD:.0f}')
config = get_config()
option = st.sidebar.radio('Opciones',
                          ['Pressura',
                           'Alternativas sustentables',
                           'Cuadro comparativo'][::-1])

horas = st.multiselect('Horario', list(range(24)), default=DEFAULT_HORAS)
meses = st.selectbox('Numero de meses', list(range(1, 7)), index=DEFAULT_MESES - 1)
 
costo_anual_electricidad = 30 * np.sum([get_costo_hora(hora) for hora in horas]) * meses
st.write(f'Costo anual electricidad: ${costo_anual_electricidad:.0f} /KW')
st.markdown('-'*50)

class StatsKeys(str):
    POTENCIA_NOMINAL = 'Potencia nominal (KW)'
    COSTO_ANUAL = 'Costo anual ($)'
    COSTO_ANUAL_USD = 'Costo anual (USD)'
    AHORRO_ANUAL_USD = 'Ahorro anual (USD)'
    COSTO_INSTALACION_USD = 'Costo instalación (USD)'

def get_stats(values):
    potencia_nominal = values['potencia_nominal']
    costo_instalacion = values['costo_instalacion']
    costo_anual = potencia_nominal * costo_anual_electricidad
    costo_anual_usd = costo_anual / USD
    ahorro_anual_usd = COSTO_ANUAL_CALDERA_USD - costo_anual_usd
    return {StatsKeys.POTENCIA_NOMINAL: potencia_nominal,
            StatsKeys.COSTO_ANUAL: costo_anual,
            StatsKeys.COSTO_ANUAL_USD: costo_anual_usd,
            StatsKeys.AHORRO_ANUAL_USD: ahorro_anual_usd,
            StatsKeys.COSTO_INSTALACION_USD: costo_instalacion
           }

def display_stats(values):
    stats = get_stats(values)
    st.write(f'Potencia nominal: {stats[StatsKeys.POTENCIA_NOMINAL]} KW')
    st.write(f'Costo anual: $ {stats[StatsKeys.COSTO_ANUAL]:.0f}')
    st.write(f'Costo anual: USD {stats[StatsKeys.COSTO_ANUAL_USD]:.0f}')
    st.write(f'Ahorro anual: USD {stats[StatsKeys.AHORRO_ANUAL_USD]:.0f}')
    st.write(f'Costo instalación: USD {values["costo_instalacion"]}')

st.header('Compra de bomba de calor')



if option == 'Pressura':
    values = config['pressura']
    display_stats(values)
elif option == 'Alternativas sustentables':
    values = config['alternativas']
    display_stats(values)
elif option == 'Cuadro comparativo':
    pressura = config['pressura']
    alt_sus = config['alternativas']
    df = pd.DataFrame([get_stats(pressura),
                       get_stats(alt_sus)],
                      index=['Pressura', 'Alternativas']).astype('int')
    st.dataframe(df,
                 use_container_width=True)
else:
    raise ValueError('`option` must be in ["Pruessura", "Alternativas sustentables"]')
