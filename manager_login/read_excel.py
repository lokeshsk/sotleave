import streamlit as st
import pandas as pd
from openpyxl import load_workbook
df = pd.read_excel('sotleaves_summary.xlsx')
st.dataframe(df)
df['Start_Date'] = pd.to_datetime(df.Start_Date)
mon = df.Start_Date.dt.to_period("M")
#book = load_workbook('sotleaves_summary1.xlsx')
writer = pd.ExcelWriter('sotleaves_summary1.xlsx', engine = 'openpyxl',mode='a')
#writer.book = book
for i , g in df.groupby(mon):
    #g.to_excel(g.Start_Date.dt.strftime('%m%y').astype(str).iloc[0] +'.xlsx',index=False)

    g.to_excel(writer, sheet_name = g.Start_Date.dt.strftime('%B-%Y').astype(str).iloc[0], index=False)
#df4.to_excel(writer, sheet_name = 'x4')
writer.close()
