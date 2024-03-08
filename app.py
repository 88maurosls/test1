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

    # Initialize session state for the input field if not already done
    if 'barcode_input' not in st.session_state:
        st.session_state['barcode_input'] = ''

    # Input field for the barcode
    barcode_input = st.text_input('Inserire il barcode', value=st.session_state.barcode_input, key='barcode_input')

    # This will change to True when the button is clicked or Enter is pressed
    perform_search = st.button('Check')

    # Placeholder for displaying the results below the search bar
    results_placeholder = st.empty()

    def on_barcode_submit():
        barcode = barcode_input
        if barcode:
            result_df = df[df['Collo'] == barcode]
            if not result_df.empty:
                st.success("TROVATA CORRISPONDENZA")
                result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
                results_placeholder.table(result_df_styled)
            else:
                st.error("CORRISPONDENZA NON TROVATA")
            # Reset the barcode input
            st.session_state.barcode_input = ''

    # If the search should be performed (either button click or Enter pressed)
    if perform_search:
        on_barcode_submit()

if __name__ == "__main__":
    main()
