import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    else:
        return [''] * len(value)

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.title("Barcode Scanner v2.1")

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

    # Verifica se la chiave 'search_query' è presente in session_state, se non lo è, la inizializza a una stringa vuota
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    # Funzione per gestire il submit della barra di ricerca
    def submit():
        # Aggiorna lo stato della ricerca con il valore attuale della barra di ricerca e resetta la barra di ricerca
        st.session_state.search_query = st.session_state.search_widget
        st.session_state.search_widget = ""

    # Barra di ricerca
    st.text_input("Cerca", key="search_widget", on_change=submit)

    # Ottiene il valore attuale della barra di ricerca dalla sessione
    search_query = st.session_state.search_query

    bar = st.text_input('Inserire il barcode')

    if st.button('Check'):
        result_df = df[df['Collo'] == bar]
        if not result_df.empty:
            st.success("Barcode TROVATO")
            # Applica la formattazione condizionale alle celle della colonna 'customer PO'
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            # Visualizzazione della tabella con Streamlit
            st.table(result_df_styled)
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

if __name__ == "__main__":
    main()
