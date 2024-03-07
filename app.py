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

    # Svuota la casella di testo "Inserire barcode" al clic del pulsante "Check" usando JavaScript
    js_clear_input = """
    <script>
    document.getElementById("barcode_input").value = "";
    </script>
    """

    # Usiamo 'key' per aggiornare dinamicamente la casella di ricerca
    bar = st.text_input('Inserire il barcode', key="barcode_input")

    if st.button('Check'):
        result_df = df[df['Collo'] == bar]
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
        # Visualizza il codice JavaScript per svuotare la casella di ricerca
        st.markdown(js_clear_input, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
