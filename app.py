import streamlit as st
import pandas as pd

def highlight_customer_po(value):
    if value.name == 'customer PO':
        return ['background-color: #f3acac'] * len(value)
    else:
        return [''] * len(value)

def display_search_results(df, barcode):
    result_df = df[df['Collo'] == barcode]
    if not result_df.empty:
        st.success("TROVATA CORRISPONDENZA")
        result_df_styled = result_df.style.apply(highlight_customer_po, axis=0)
        st.table(result_df_styled)
    else:
        st.error("CORRISPONDENZA NON TROVATA")
    return not result_df.empty

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

    barcode = st.text_input('Inserire il barcode', value="", key="barcode_input")

    if st.button('Check') or st.session_state.get('submitted', False):
        if barcode:
            found = display_search_results(df, barcode)
            if found:
                # Reset the input field after successful search
                st.session_state.barcode_input = ""
            # This state variable is used to ensure we only reset the barcode after a submission
            st.session_state.submitted = True
    else:
        # Ensure the submitted state is False unless the button is pressed
        st.session_state.submitted = False

if __name__ == "__main__":
    main()
