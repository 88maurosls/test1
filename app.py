import streamlit as st
import pandas as pd

def load_data(sheet_id, sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    # Specifica manualmente il tipo di dati delle colonne durante il caricamento del CSV
    dtype_dict = {'Collo': str}  
    # Utilizza la funzione `converters` per specificare il tipo di dati della colonna 'customer PO' come `object`
    converters = {'customer PO': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("Frenz's Barcode App V2")

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'

    df = load_data(SHEET_ID, SHEET_NAME)

    bar = st.text_input('Inserire il barcode')

    if st.button('Check'):
        if not df[df['Collo'] == bar].empty:
            st.success("Barcode TROVATO:")
            st.dataframe(df[df['Collo'] == bar])
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

if __name__ == "__main__":
    main()
