import streamlit as st
import pandas as pd

def main():
    st.set_page_config(layout="wide")
    st.title("Frenz's Barcode App V2")

    # ID e nome del foglio del Google Sheet
    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    # Lettura dei dati da Google Sheets
    df = pd.read_csv(url, dtype={'Collo': str, 'Customer PO': str})

    # Assicurati che tutti i valori in 'Customer PO' siano letti come stringhe
    df['Customer PO'] = df['Customer PO'].astype(str)

    # Rimuovere eventuali spazi vuoti iniziali o finali nei dati
    df['Customer PO'] = df['Customer PO'].str.strip()

    bar = st.text_input('Inserire il barcode')

    if st.button('Check'):
        if not df[df['Collo'] == bar].empty:
            st.success("Barcode TROVATO:")
            # Puoi rimuovere l'indice reset_index(drop=True) se desideri mantenere l'indice originale
            st.dataframe(df[df['Collo'] == bar].reset_index(drop=True))
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

if __name__ == "__main__":
    main()
