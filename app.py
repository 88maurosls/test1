import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    else:
        return [''] * len(value)

def check_barcode():
    barcode = st.session_state.barcode_input
    if barcode:
        st.write("Barcode cercato:", barcode)
        result_df = df[df['Collo'] == barcode]
        if not result_df.empty:
            st.success("TROVATA CORRISPONDENZA")
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            st.table(result_df_styled)
        else:
            st.error("CORRISPONDENZA NON TROVATA")

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.title("Dope Barcode Scanner v2.4")

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    # Specifica manualmente il tipo di dati delle colonne durante il caricamento del CSV
    dtype_dict = {'Collo': str}  
    # Utilizza la funzione `converters` per specificare il tipo di dati della colonna 'UPC' come `str`
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)

    # Ordina le colonne nel DataFrame
    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date', 'Rif. Sped.']]

    # Inizializzazione dello stato della sessione per il campo di input del barcode
    if 'barcode_input' not in st.session_state:
        st.session_state.barcode_input = ''

    # Barra di ricerca del barcode
    st.text_input('Inserire il barcode', key='barcode_input', on_change=check_barcode)

    if st.button('Check'):
        check_barcode()

if __name__ == "__main__":
    main()
