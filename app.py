import streamlit as st
import pandas as pd

#https://docs.google.com/spreadsheets/d/1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ/edit

def main():
    st.set_page_config(layout="wide")
    st.title("Frenz's Barcode App V2")
    st.image('barcode.png')

    SHEET_ID = '1Ps6OqL1cLdCiD30VJTkDhSWKNYW2I7Uqhg1viCBvFXQ'
    SHEET_NAME = 'test'
    foglio_id=0
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}/edit#gid={foglio_id}'
    df = pd.read_csv(url,dtype={'Collo':str})
    bar = st.text_input('inserire il barcode')
    #bar = "00008865511394193353" #testing
    if st.button('check'):
        if not df[df['Collo'] == bar].empty:
            st.balloons()
            st.success("Barcodes TROVATO:")
            st.dataframe(df[df['Collo']==bar])
        else:
            st.error("BARCODE NON TROVATO!!!!!!")
            #################################################

if __name__ == '__main__':
    main()
