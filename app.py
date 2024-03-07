import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    else:
        return [''] * len(value)

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.title("Barcode Scanner v2.0")

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    dtype_dict = {'Collo': str}  
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)

    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date']]

    # Utilizza st.empty() per creare un placeholder per la casella di ricerca
    bar_input = st.text_input('Inserire il barcode')

    # Aggiungi un pulsante "Reset" per cancellare il valore della casella di ricerca
    if st.button('Reset'):
        bar_input = ''

    if st.button('Check'):
        result_df = df[df['Collo'] == bar_input]
        if not result_df.empty:
            st.success("Barcode TROVATO")
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            if len(result_df) > 10:
                st.dataframe(result_df_styled)
            else:
                st.dataframe(result_df_styled, height=None)
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

    # Inserisci CSS personalizzato direttamente tramite st.markdown
    st.markdown("""
    <style>
        body {
            font-family: A
