import streamlit as st
import pandas as pd

def main():
    st.set_page_config(layout="wide")
    st.title("Frenz's Barcode App V2")

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    # Tentativo di specificare una codifica e gestire valori nulli
    df = pd.read_csv(url, dtype={'Collo': str, 'Customer PO': str}, encoding='utf-8', na_filter=False)

    # Stampa dei dati grezzi per il debug
    st.write(df.head())  # Stampa le prime cinque righe per il debug

    bar = st.text_input('Inserire il barcode')

    if st.button('Check'):
        result = df[df['Collo'] == bar]
        if not result.empty:
            st.success("Barcode TROVATO:")
            st.dataframe(result)
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

if __name__ == "__main__":
    main()
