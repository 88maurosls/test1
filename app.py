import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    """Questa funzione evidenzia le celle della colonna 'customer PO'."""
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    return [''] * len(value)

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.title("Dope Barcode Scanner v2.4")

    # Caricamento dei dati dal foglio Google Sheets
    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    dtype_dict = {'Collo': str}
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)
    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date', 'Rif. Sped.']]

    # Definizione della barra di ricerca
    barcode_input = st.text_input('Inserire il barcode', key='barcode_input')

    # Definizione del pulsante di ricerca
    check_button = st.button('Check')

    # Placeholder per i risultati di ricerca
    results_placeholder = st.empty()

    # Se il pulsante viene premuto oppure c'è un input
    if check_button or barcode_input:
        barcode = st.session_state.barcode_input
        if barcode:
            # Ricerca del barcode
            result_df = df[df['Collo'] == barcode]
            # Se non vuoto, mostra i risultati
            if not result_df.empty:
                st.success("TROVATA CORRISPONDENZA")
                # Applicazione dello stile condizionale
                result_df_styled = result_df.style.apply(highlight_customer_po, axis=1)
                results_placeholder.table(result_df_styled.render())  # Visualizzazione dei risultati
            else:
                st.error("CORRISPONDENZA NON TROVATA")
            # Reset del campo di input
            st.session_state.barcode_input = ''

if __name__ == "__main__":
    main()
