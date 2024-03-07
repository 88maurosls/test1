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

    # Specifica manualmente il tipo di dati delle colonne durante il caricamento del CSV
    dtype_dict = {'Collo': str}  
    # Utilizza la funzione `converters` per specificare il tipo di dati della colonna 'UPC' come `str`
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)

    # Ordina le colonne nel DataFrame
    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date']]

    bar1 = st.text_input('Inserire il barcode 1')

    if st.button('Check 1'):
        result_df = df[df['Collo'] == bar1]
        if not result_df.empty:
            st.success("Barcode TROVATO")
            # Applica la formattazione condizionale alle celle della colonna 'customer PO'
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            # Visualizzazione della tabella con Streamlit
            if len(result_df) > 10:
                st.dataframe(result_df_styled)
            else:
                st.dataframe(result_df_styled, height=None)
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

    bar2 = st.text_input('Inserire il barcode 2')

    if st.button('Check 2'):
        result_df = df[df['Collo'] == bar2]
        if not result_df.empty:
            st.success("Barcode TROVATO")
            # Applica la formattazione condizionale alle celle della colonna 'customer PO'
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            # Visualizzazione della tabella con Streamlit
            if len(result_df) > 10:
                st.dataframe(result_df_styled)
            else:
                st.dataframe(result_df_styled, height=None)
        else:
            st.error("BARCODE NON TROVATO!!!!!!")
            # Pulisci il contenuto della prima barra di ricerca
            st.text_input('Inserire il barcode 1', value='')

if __name__ == "__main__":
    main()
