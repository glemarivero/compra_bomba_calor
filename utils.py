import streamlit as st

def get_costo_hora(hora):
    if 0 <= hora < 7:
        return 2.303
    elif 7 <= hora < 18 or 22 <= hora < 24:
        return 5.068
    else:
        return 11.531
