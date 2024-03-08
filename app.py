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

    # Specifica manualmente il tipo di dati delle colonne durante il caricamento del CSV
    dtype_dict = {'Collo': str}  
    # Utilizza la funzione `converters` per specificare il tipo di dati della colonna 'UPC' come `str`
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)

    # Ordina le colonne nel DataFrame
    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date', 'Rif. Sped.']]

    # Barra di ricerca del barcode
    barcode_input = st.text_input('Inserire il barcode')

    check_button_pressed = st.button('Check')

    last_button_pressed = st.session_state.get('last_button_pressed', '')

    if barcode_input != "" and (last_button_pressed == 'Check' or last_button_pressed == 'Enter'):
        check_barcode(barcode_input, df)
        st.session_state.barcode_input = ""

    if check_button_pressed:
        st.session_state.last_button_pressed = 'Check'

def check_barcode(barcode_input, df):
    bar = barcode_input.strip()  # Rimuovi spazi bianchi all'inizio e alla fine
    if bar:  # Verifica se il valore della barra di ricerca non è vuoto
        st.write("Barcode cercato:", bar)  # Visualizza il valore inserito nella barra di ricerca
        result_df = df[df['Collo'] == bar]
        if not result_df.empty:
            st.success("TROVATA CORRISPONDENZA")
            # Applica la formattazione condizionale alle celle della colonna 'customer PO'
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            # Visualizzazione della tabella con Streamlit
            st.table(result_df_styled)
        else:
            st.error("CORRISPONDENZA NON TROVATA")

if __name__ == "__main__":
    main()
