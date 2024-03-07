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
    df = pd.read_csv(url)

    # Stampa i nomi delle colonne per assicurarti che siano corretti
    st.write(df.columns)

    # Assicurati di utilizzare il nome esatto della colonna come appare nel DataFrame
    # Ad esempio, se il nome della colonna è 'customer PO' invece di 'Customer PO'
    df['customer PO'] = df['customer PO'].astype(str)

    bar = st.text_input('Inserire il barcode')

    if st.button('Check'):
        if not df[df['Collo'] == bar].empty:
            st.success("Barcode TROVATO:")
            st.dataframe(df[df['Collo'] == bar].reset_index(drop=True))
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

if __name__ == "__main__":
    main()
