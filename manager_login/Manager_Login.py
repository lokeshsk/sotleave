#import streamlit_authenticator as stauth
import streamlit as st
import mysql.connector
import pandas as pd
#import pymysql
import hashlib
import os.path
from leave_update import leave_status_1
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
# leave_status_1()
st.set_page_config(
    page_title="Manager Login",
    page_icon="📝",
    layout="wide"
)

file = os.path.isfile('username.txt') 
#st.write(file)
#if 'username' not in st.session_state:
#    st.session_state['username'] = ''

def db_connect():
    conn =mysql.connector.connect(host="localhost",
    user="root", 
    password="", 
    db="leaves")
    return conn

mydb = db_connect()
mycursor = mydb.cursor()
  
def fetch_db(option):
    #st.write(data)
    # if option=='Pending':
        # newval =2
    # elif option=='Approved':
        # newval=1
    # else:
        # newval=0
    qry = "select ID, eid, ename, no_days,start_date,end_date, reason,cleaves from leave_records where status=%s"
    val = (option,)
    mycursor.execute(qry, val)
    res = mycursor.fetchall()
    return res

if file==False:
    st.sidebar.write("# Manager Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password",type='password')
    s = hashlib.sha3_256()
    password = password.encode()
    s.update(password)
    hashpass = s.hexdigest()
    if st.sidebar.button("Login"):
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        values = (username, hashpass)
        mycursor.execute(query, values)
        record = mycursor.fetchone()
        
        if record:
                #st.write("hello")
                st.write("# Manager Portal")
                streamlit_js_eval(js_expressions="parent.window.location.reload()")
                st.sidebar.success("Logged in as {}".format(username))
                #st.session_state.username=username
              
                with open('username.txt', 'w') as f:
                    f.write(username)
                option = st.selectbox('Select to check the status',('pending', 'approved', 'rejected'))
                st.write('You selected:', option)
                res = fetch_db(option)
                headers =  ["Emp_ID","Employee_Name","No_Days","Start_Date","End_Date","Reason","Compensatory_Dates"]
                #res.columns = headers
                df = pd.DataFrame(res, columns=headers)
                df['Emp_ID'] = df['Emp_ID'].astype(str)
                df['Emp_ID'] = df['Emp_ID'].replace(",", "") 
                df['Start_Date'] = pd.to_datetime(df.Start_Date)
                df['Start_Date']=df['Start_Date'].dt.strftime('%d-%m-%Y')
                df['End_Date'] = pd.to_datetime(df.End_Date)
                df['End_Date']=df['End_Date'].dt.strftime('%d-%m-%Y')
                #df['App_Date'] = pd.to_datetime(df.App_Date)
                #df['App_Date']=df['App_Date'].dt.strftime('%d-%m-%Y')
                if option=='pending':
                    df['Approved']=False
                    df['Rejected']=False
                    edited_df = st.data_editor(df)
                    approved = edited_df.loc[edited_df["Approved"]==True]["Request_ID"]
                    rejected = edited_df.loc[edited_df["Rejected"]==True]["Request_ID"]
                    emp_id_approved = edited_df.loc[edited_df["Approved"]==True]["Emp_ID"]
                    emp_id_rejected = edited_df.loc[edited_df["Rejected"]==True]["Emp_ID"]
                    emp_name_approved = edited_df.loc[edited_df["Approved"]==True]["Employee_Name"]
                    emp_name_rejected = edited_df.loc[edited_df["Rejected"]==True]["Employee_Name"]
                    if any(approved):
                        newdf = pd.Series(list(approved))
                        newdf1 = pd.Series(list(emp_id_approved))
                        newdf2 = pd.Series(list(emp_name_approved))
                        #st.write(newdf[4])
                        id1 = int(newdf[0])
                        empa = int(newdf1[0])
                        empname_approved = newdf2[0]
                        leave_status_1(empa,empname_approved,'approved')
                        qry2 = "UPDATE leave_records SET status = 'approved' WHERE ID= %s"
                        val2 = (id1,)
                        mycursor.execute(qry2, val2)
                        mydb.commit()
                        
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
                    elif any(rejected):
                        newdf = pd.Series(list(rejected))
                        newdf1 = pd.Series(list(emp_id_rejected))
                        newdf2 = pd.Series(list(emp_name_rejected))
                        #st.write(newdf[4])
                        id1 = int(newdf[0])
                        empr = int(newdf1[0])
                        empname_rejected = newdf2[0]
                        leave_status_1(empr,empname_rejected,'rejected')
                        qry2 = "UPDATE leave_records SET status = 'rejected' WHERE ID= %s"
                        val2 = (id1,)
                        mycursor.execute(qry2, val2)
                        mydb.commit()
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
                    # else:
                        # pass
                else:
                    st.dataframe(df)
        else:
            flag=0
            st.sidebar.warning("Incorrect username or password")
else:
    f = open("username.txt")
    username = f.readline()
    f.close()
    st.write("# Manager Portal")
    st.sidebar.success("Logged in as {}".format(username))
    logout = st.sidebar.button(label="Logout")
    if logout:
        os.remove('username.txt')
    option = st.selectbox('Select to check the status',('Pending', 'Approved', 'Rejected'))
    st.write('You selected:', option)
    res = fetch_db(option)
    headers =  ["Request_ID","Emp_ID","Employee_Name","No_Days","Start_Date","End_Date","Reason","Compensatory_Dates"]
    #res.columns = headers
    df = pd.DataFrame(res, columns=headers)
    df['Emp_ID'] = df['Emp_ID'].astype(str)
    df['Emp_ID'] = df['Emp_ID'].replace(",", "") 
    df['Start_Date'] = pd.to_datetime(df.Start_Date)
    df['Start_Date']=df['Start_Date'].dt.strftime('%d-%m-%Y')
    df['End_Date'] = pd.to_datetime(df.End_Date)
    df['End_Date']=df['End_Date'].dt.strftime('%d-%m-%Y')
    #df['App_Date'] = pd.to_datetime(df.App_Date)
    #df['App_Date']=df['App_Date'].dt.strftime('%d-%m-%Y')
    #st.write(df)
    
    if option=='Pending':
        df['Approved']=False
        df['Rejected']=False
        edited_df = st.data_editor(df)
        approved = edited_df.loc[edited_df["Approved"]==True]["Request_ID"]
        rejected = edited_df.loc[edited_df["Rejected"]==True]["Request_ID"]
        emp_id_approved = edited_df.loc[edited_df["Approved"]==True]["Emp_ID"]
        emp_id_rejected = edited_df.loc[edited_df["Rejected"]==True]["Emp_ID"]
        emp_name_approved = edited_df.loc[edited_df["Approved"]==True]["Employee_Name"]
        emp_name_rejected = edited_df.loc[edited_df["Rejected"]==True]["Employee_Name"]
        if any(approved):
            newdf = pd.Series(list(approved))
            newdf1 = pd.Series(list(emp_id_approved))
            newdf2 = pd.Series(list(emp_name_approved))
            #st.write(newdf[4])
            id1 = int(newdf[0])
            empa = int(newdf1[0])
            empname_approved = newdf2[0]
            leave_status_1(empa,empname_approved,'approved')
            # st.warning(sa, icon="⚠️")
            qry2 = "UPDATE leave_records SET status = 'approved' WHERE ID= %s"
            val2 = (id1,)
            mycursor.execute(qry2, val2)
            mydb.commit()       
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
        elif any(rejected):
            newdf = pd.Series(list(rejected))
            newdf1 = pd.Series(list(emp_id_rejected))
            newdf2 = pd.Series(list(emp_name_rejected))
            #st.write(newdf[4])
            id1 = int(newdf[0])
            empr = int(newdf1[0])
            empname_rejected = newdf2[0]
            leave_status_1(empr,empname_rejected,'rejected')
            
            qry2 = "UPDATE leave_records SET status = 'rejected' WHERE ID= %s"
            val2 = (id1,)
            mycursor.execute(qry2, val2)
            mydb.commit()
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
    else:
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
