import streamlit as st
import pandas as pd
df = pd.read_csv(r"../emp_records/emp_records.csv", header=0)
# df = pd.read_csv('emp_records.csv')
df = df.astype('str')
df['E_ID']= df['E_ID'].str.replace(',','',regex=True)
df = df.sort_values(by=['E_ID'])
st.dataframe(df) 