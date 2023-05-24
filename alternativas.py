import streamlit as st

def main():
    empresa = 'alternativas'
    modelo = 'RS-038TA1'
    potencia_nominal = 24.9 * 3
    potencia_nominal_calorifica = 108
    costo_instalacion = 43940

    return dict(modelo=modelo,
                empresa=empresa,
                potencia_nominal_calorifica=potencia_nominal_calorifica,
                potencia_nominal=potencia_nominal,
                costo_instalacion=costo_instalacion)
