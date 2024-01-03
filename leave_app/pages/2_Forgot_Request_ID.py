import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(
    page_title="Search Request ID",
    page_icon="📝",
)

st.write("# Forgot/Search Request ID")
def db_connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="leaves"
    )
    return mydb
    
def fetch_db(data: dict):
    #st.write(data)
    mydb = db_connect()
    mycursor = mydb.cursor()
    qry = "select ID, ename, app_date from leave_records where ename like %s"
    val = ('%'+data['req_name']+'%',)
    mycursor.execute(qry, val)
    res = mycursor.fetchall()
    return res
    
    
form = st.form(key="match")
with form:

    req_id = st.text_input('Enter Your Name', placeholder ='Enter Name')
    #streamlit_js_eval(js_expressions="parent.window.location.reload()")
    submit = st.form_submit_button("Submit")
    if submit:
        res = fetch_db({"req_name":str(req_id)})
        headers =  ["Request_ID","Employee_Name", "Date_of_Application"]
        #res.columns = headers
        df = pd.DataFrame(res, columns= headers)
        if df.empty:
            st.error("No records found")
        else:
            df['Date_of_Application'] = pd.to_datetime(df.Date_of_Application)
            df['Date_of_Application']=df['Date_of_Application'].dt.strftime('%d-%m-%Y')
            st.dataframe(df)
        
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