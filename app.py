import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    else:
        return [''] * len(value)

def search(df, barcode):
    result_df = df[df['Collo'] == barcode]
    if not result_df.empty:
        st.success("TROVATA CORRISPONDENZA")
        result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
        return result_df_styled
    else:
        st.error("CORRISPONDENZA NON TROVATA")
        return None

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

    if 'barcode_input' not in st.session_state:
        st.session_state['barcode_input'] = ''

    def on_barcode_submit():
        if st.session_state.barcode_input:
            result_df_styled = search(df, st.session_state.barcode_input)
            if result_df_styled is not None:
                st.write("Barcode cercato:", st.session_state.barcode_input)
                st.table(result_df_styled)
            st.session_state.barcode_input = ''  # Clear the input box

    barcode_input = st.text_input('Inserire il barcode', value=st.session_state.barcode_input, on_change=on_barcode_submit, key='barcode')

    if st.button('Check'):
        on_barcode_submit()  # Chiama la funzione manualmente

if __name__ == "__main__":
    main()
