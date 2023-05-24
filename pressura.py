import streamlit as st

def main():
    empresa = 'pressura'
    modelo = 'nordflux'
    potencia_nominal_calorifica = 90
    potencia_nominal = 28.3 * 3
    costo_instalacion = 35426 * 1.22
    return dict(modelo=modelo,
                empresa=empresa,
                potencia_nominal_calorifica=potencia_nominal_calorifica,
                potencia_nominal=potencia_nominal,
                costo_instalacion=costo_instalacion)
