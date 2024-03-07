import streamlit as st
import pandas as pd

def main():
    st.set_page_config(layout="wide")
    st.title("Frenz's Barcode App V2")

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    # Specifica esplicitamente i tipi di dati delle colonne durante la lettura
    dtype_dict = {'Collo': str, 'Customer PO': str}  # Aggiungi altre colonne se necessario
    df = pd.read_csv(url, dtype=dtype_dict)

    bar = st.text_input('Inserire il barcode')

    if st.button('Check'):
        if not df[df['Collo'] == bar].empty:
            st.success("Barcode TROVATO:")
            st.dataframe(df[df['Collo'] == bar])
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

if __name__ == "__main__":
    main()
