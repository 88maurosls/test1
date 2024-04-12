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

    SHEET_ID = '1FTlnrfpO5UJXaTyTQ-S-sCwkbf9zGC-DluTGKLnDVfo'
    SHEET_NAME = 'Divisione2'
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
        st.session_state.show_results = False  # Variabile di stato per controllare se mostrare i risultati

    # Barra di ricerca del barcode
    if 'barcode_input' not in st.session_state:
        st.session_state.barcode_input = ''
    def submit():
        st.session_state.barcode_input = st.session_state.widget
        st.session_state.widget = ''
        st.session_state.show_results = True  # Imposta show_results su True quando l'utente invia il barcode

    st.text_input('Inserire il barcode', key='widget', on_change=submit)

    if st.session_state.show_results:
        check_barcode(df, st.session_state.barcode_input)  # Chiamata alla funzione check_barcode se show_results è True

def check_barcode(df, bar):
    if bar:
        st.write("Barcode cercato:", bar)  # Visualizza il valore inserito nella barra di ricerca
        result_df = df[df['Collo'] == bar]  # Utilizza 'Collo' per trovare la corrispondenza
        if not result_df.empty:
            st.success("TROVATA CORRISPONDENZA")
            # Applica la formattazione condizionale alle celle della colonna 'customer PO'
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            # Visualizzazione della tabella con Streamlit
            st.table(result_df_styled)

            # Ottiene il 'Rif. Sped.' corrispondente al 'Collo' scansionato
            shipping_ref = result_df['Rif. Sped.'].iloc[0]
            # Seleziona tutti i record con lo stesso 'Rif. Sped.'
            all_orders = df[df['Rif. Sped.'] == shipping_ref]
            # Controlla se tutti questi record hanno lo stesso 'customer PO'
            unique_customer_pos = all_orders['customer PO'].unique()
            if len(unique_customer_pos) == 1:
                customer_po = unique_customer_pos[0]
                st.info(f"PACKING TUTTA DI {customer_po}")
            else:
                customer_po_list = ', '.join(unique_customer_pos)
                st.info(f"Questa packing contiene ordini di {customer_po_list}")
        else:
            st.error("CORRISPONDENZA NON TROVATA")



if __name__ == "__main__":
    main()
