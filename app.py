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

    dtype_dict = {'Collo': str}
    converters = {'customer PO': str, 'UPC': str}
    df = pd.read_csv(url, dtype=dtype_dict, converters=converters)

    df = df[['Collo', 'customer PO', 'SKU', 'Size', 'Unità', 'UPC', 'Made in', 'Import Date']]

    # Check if 'clear_bar' key exists in session state, if not, initialize it.
    if 'clear_bar' not in st.session_state:
        st.session_state.clear_bar = False

    # Create a text input that is tied to the 'clear_bar' state.
    bar = st.text_input('Inserire il barcode', value="" if st.session_state.clear_bar else None, key='barcode_input')

    # Check barcode against the dataframe.
    if st.button('Check'):
        st.session_state.clear_bar = True  # Set the flag to clear the bar next time it's clicked on.
        result_df = df[df['Collo'] == bar]
        if not result_df.empty:
            st.success("Barcode TROVATO")
            result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
            st.dataframe(result_df_styled)
        else:
            st.error("BARCODE NON TROVATO!!!!!!")

    # If the user interacts with the text input and 'clear_bar' is True, clear the text input.
    if bar and st.session_state.clear_bar:
        st.session_state.clear_bar = False  # Reset the flag as the bar has been cleared.

if __name__ == "__main__":
    main()
