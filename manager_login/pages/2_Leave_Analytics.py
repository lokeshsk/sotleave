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
import matplotlib.pyplot as plt

#import streamlit_ext as ste
st.set_page_config(
    page_title="Leave Analytics",
    page_icon="📝",
    layout="wide",
)

st.write("# SOT Leaves Analytics")

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
    qry = "select  ename, eid,start_date, end_date, no_days from leave_records where status = 'approved'"
    mycursor.execute(qry)
    res = mycursor.fetchall()
    return res

#Displaying leaves summary (approved)
def highlight_survived(s):
    return ['background-color: pink']*len(s) if s.No_Days > 5 else ['background-color: lightgreen']*len(s)


res = fetch_db()

option = st.selectbox(
    'Choose the month',
    ('January', 'February', 'March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December','All Months'))


# st.write("Current month analytics:")
headers =  ["Emp.name", "E.ID", "Start_Date","End_Date", "No_Days"]
# df['Start_Date'] = pd.to_datetime(df.Start_Date, format='%d-%m-%Y')
df = pd.DataFrame(res, columns= headers)

df['Start_Date'] = pd.to_datetime(df.Start_Date, format='%d-%m-%Y')

mon = df.Start_Date.dt.to_period("M")
for i , g in df.groupby(mon):
    monthdf = g.Start_Date.dt.strftime('%B').astype(str).iloc[0]
    month_year = g.Start_Date.dt.strftime('%B-%Y').astype(str).iloc[0]
    if monthdf == option:
        df = g.drop(['Start_Date', 'End_Date'], axis=1)
        # st.write(df)
        df2 = df.groupby('E.ID').sum()
        df2 = df2.sort_values(['No_Days'], ascending=[False])
        df2['No_Days'] = df2["No_Days"].astype('int')
        st.dataframe(df2.style.apply(highlight_survived, axis=1),use_container_width=True)
    elif option == 'All Months':
        st.write(month_year)
        df = g.drop(['Start_Date', 'End_Date'], axis=1)
        # st.write(df)
        df2 = df.groupby('E.ID').sum()
        df2 = df2.sort_values(['No_Days'], ascending=[False])
        df2['No_Days'] = df2["No_Days"].astype('int')
        st.dataframe(df2.style.apply(highlight_survived,axis=1),use_container_width=True)
                    # st.error("No data is available")


#plt.show()
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