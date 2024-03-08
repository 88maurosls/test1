import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    else:
        return [''] * len(value)

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.title("Dope Barcode Scanner v2.4")

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    dtype_dict = {'Collo': str}  
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)
    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date', 'Rif. Sped.']]

    # Barra di ricerca del barcode
    barcode = st.text_input('Inserire il barcode', key='barcode_input')

    # Placeholder per i risultati di ricerca
    results_placeholder = st.empty()

    def search_and_display(barcode):
        st.session_state.barcode_input = barcode  # Aggiorna il valore nello stato della sessione
        if barcode:
            result_df = df[df['Collo'] == barcode]
            if not result_df.empty:
                st.success("TROVATA CORRISPONDENZA")
                result_df_styled = result_df.style.apply(highlight_customer_po, axis=1)
                results_placeholder.table(result_df_styled)
            else:
                st.error("CORRISPONDENZA NON TROVATA")
            st.session_state.barcode_input = ''  # Reset del campo di input dopo la visualizzazione dei risultati

    # Pulsante per la ricerca
    if st.button('Check'):
        search_and_display(barcode)

    # Azione del tasto Invio
    if barcode and (barcode != st.session_state.get('last_barcode')):
        st.session_state.last_barcode = barcode  # Memorizza l'ultimo barcode inserito
        search_and_display(barcode)

if __name__ == "__main__":
    main()
