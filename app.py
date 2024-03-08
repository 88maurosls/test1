import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

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

    # Verifica se la chiave 'barcode_input' è presente in session_state, se non lo è, la inizializza a una stringa vuota
    if "barcode_input" not in st.session_state:
        st.session_state.barcode_input = ""

    # Barra di ricerca del barcode
    if 'barcode_input' not in st.session_state:
        st.session_state.barcode_input = ''

    # Casella di testo per l'inserimento del barcode
    barcode_input = st.text_input('Inserire il barcode', key='widget', value=st.session_state.barcode_input)

    # Codice JavaScript per triggerare il clic del pulsante "Search" alla pressione del tasto "Enter"
    script = """
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const textInput = document.querySelector("[data-testid='stTextInput']");
            const button = document.querySelector("[data-testid='stButton']");
            textInput.addEventListener("keypress", function(e) {
                if (e.key === "Enter") {
                    button.click();
                }
            });
        });
    </script>
    """
    st.markdown(script, unsafe_allow_html=True)

    # Pulsante per avviare la ricerca
    if st.button('Search'):
        submit(barcode_input)

def submit(value):
    st.session_state.barcode_input = value
    bar = st.session_state.barcode_input
    df = get_dataframe()  # Funzione da implementare per ottenere il DataFrame
    if bar:
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
