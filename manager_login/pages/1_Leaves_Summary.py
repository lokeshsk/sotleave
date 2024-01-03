import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
from datetime import datetime
from time import time 
import os.path
import calendar
from openpyxl import load_workbook
import numpy as np

#import streamlit_ext as ste
st.set_page_config(
    page_title="Leave Summary",
    page_icon="📝",
)

st.write("# SOT Leaves Summary")

def db_connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="leaves"
    )
    return mydb
    
mydb = db_connect()
mycursor = mydb.cursor()

def fetch_db():
    qry = "select ID, app_date, ename, eid,start_date, end_date, no_days, reason, nature from leave_records where status = 'approved'"
    mycursor.execute(qry)
    res = mycursor.fetchall()
    return res

#Displaying leaves summary (approved)

res = fetch_db()
headers =  ["ID","App_Date", "Emp.name", "E.ID", "Start_Date","End_Date", "No_Days", "Reason","Leave_Type"]
df = pd.DataFrame(res, columns= headers)
df['App_Date'] = pd.to_datetime(df.App_Date)
df['App_Date']=df['App_Date'].dt.strftime('%d-%m-%Y')
df['Start_Date'] = pd.to_datetime(df.Start_Date, format='%d-%m-%Y')
#df['Start_Date']=df['Start_Date'].dt.strftime('%d-%m-%Y')
#df['Start_Date'] = pd.to_datetime(df.Start_Date, format='%d-%m-%Y')
df['End_Date'] = pd.to_datetime(df.End_Date)
df['End_Date']=df['End_Date'].dt.strftime('%d-%m-%Y')
st.dataframe(df)

mon = df.Start_Date.dt.to_period("M")
#book = load_workbook('sotleaves_summary1.xlsx')
writer = pd.ExcelWriter('sotleaves_summary.xlsx', engine = 'openpyxl',mode='a',if_sheet_exists='replace')
#writer.book = book
for i , g in df.groupby(mon):
    #g.to_excel(g.Start_Date.dt.strftime('%m%y').astype(str).iloc[0] +'.xlsx',index=False)

    g.to_excel(writer, sheet_name = g.Start_Date.dt.strftime('%B-%Y').astype(str).iloc[0], index=False)
#df4.to_excel(writer, sheet_name = 'x4')
writer.close()

#Download button for excel file

file_path="sotleaves_summary.xlsx"
def download(file_path):
    with open(file_path, 'rb') as excel_file:
        st.download_button(label = 'Download File', data = excel_file, file_name ='sotleaves_summary.xlsx', mime= 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  

download(file_path)

footer="""<style>
a:link , a:visited{
color: yellow;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: orange;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
height:40px;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: inline; text-align: center;' href="https://sites.google.com/view/lokeshkumar" target="_blank">Lokesh Kumar</a> and <a style='display: inline; text-align: center;' href="#" target="_blank">Amogh Deshmukh</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton{visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 