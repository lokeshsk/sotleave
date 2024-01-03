import streamlit as st
import mysql.connector
import pandas as pd
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
import base64
from datetime import date
from datetime import datetime
from time import time 
import os
from random import randint
import csv
from email.message import EmailMessage
import smtplib
import ssl

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    


#import streamlit_ext as ste
st.set_page_config(
    page_title="Leave Status",
    page_icon="📝",
    layout="wide"
)

st.write("# Delete Leave Request")

#req_id=''
#pdffile=''

 
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

def fetch_db(data: dict):
    #st.write(data)
    # mydb = db_connect()
    # mycursor = mydb.cursor()
    qry = "select ID, app_date, ename, eid, designation, department, manager,start_date, end_date, no_days, reason, work_done, nature, esign,cleaves ,status  from leave_records where ID = %s"
    val = (data['req_id'],)
    mycursor.execute(qry, val)
    res = mycursor.fetchall()
    return res





#with form:
pdffile=''
#req_id = st.text_input('Enter Request ID', placeholder ='Enter Request ID')
st.divider()
def send_email():
    res1 = fetch_db({"req_id":str(req_id)})
    headers1 =  ["ID","App_Date", "Emp.name", "E.ID", "Designation", "Department", "Manager", "Start_Date","End_Date", "No_Days", "Reason","Work_Done_By","Leave_Type","File","Compensatory_Leave_Dates", "Status"]
    df1 = pd.DataFrame(res1, columns= headers1)
    if df1.empty:
        st.error("No records found")
    else:
        #st.dataframe(df)
        x=df1.to_dict()
        if x['Status'][0] == "approved":
            empname = x['Emp.name'][0]
            empar = x['E.ID'][0]
            dfemp = pd.read_csv(r"../emp_records/emp_records.csv", header=0)
            e_s=dfemp[dfemp['E_ID']==empar]
            # st.write(e_s['E_EMAIL'])
            emp_email = e_s['E_EMAIL']
            if(emp_email.empty):
                st.write("Automated email was not sent, as your email is missing.")
            else:
                df2 = pd.read_csv("otp.csv")
                df2 = df2.astype('str')
                df2['OTP']= df2['OTP'].str.replace(',','',regex=True)
                record2 = df2[df2['REQ_ID']==str(req_id)]
                x = int(record2['OTP'])
                email_sender = 'sot.leave@gmail.com'
                email_password = 'cpbo msgi jaek dywh'
                email_receiver = emp_email

                # Set the subject and body of the email
                subject = 'OTP - SOT Leave APP'
                body = """
                Dear {employeename},
                
                Your OTP to delete request is {x}.

                Note: This is an auto-generated mail. Kindly do not reply to this mail.

                Regards,
                SOT-APP
                """.format(employeename=empname, x = x)

                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                
                em['Subject'] = subject
                
                em.set_content(body)

                # Add SSL (layer of security)
                context = ssl.create_default_context()

                # Log in and send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string()) 

                    st.success("OTP sent successfully to your mail id.")


        elif x['Status'][0] == "pending":
            st.error("Your request is still pending.")
        else:
            st.error("Your request is rejected.")
    




col1, col2,col3 = st.columns(3)

flag=0
with col1:
    st.write('##### Step-1: Generate OTP')
    with st.form('Form1'):
        req_id = st.text_input('Request ID',placeholder="Request ID")
        submit = st.form_submit_button("Generate OTP", type='primary')   
        if submit:
            
            ver_otp = random_with_N_digits(6)
            df1 = pd.read_csv("otp.csv")
            record1 = df1['REQ_ID'].to_list()
            list_int = map(int, record1) 
            #st.write(list_int)
            req_id = int(req_id)
            # st.write(req_id)
            # st.write(type(req_id))
            #st.write(ver_otp)
            if int(req_id) not in record1:
                f = open("otp.csv","a", newline='')
                csvwriter = csv.writer(f) 
                fields=[req_id,ver_otp]
                csvwriter.writerow(fields)  
                f.close()
                send_email()
                #st.write(ver_otp)
            else:
                send_email()
        #if st.button("Verify"):
        #verify()
        
                #verify()
with col2:
    st.write('##### Step-2: Verify OTP')
    with st.form('Form2'):
        otp = st.text_input('Enter OTP',placeholder="OTP")
        submit = st.form_submit_button("Verify OTP", type='primary')
        if submit:

            df = pd.read_csv("otp.csv")
            df = df.astype('str')
            df['OTP']= df['OTP'].str.replace(',','',regex=True)
            record = df[df['REQ_ID']==str(req_id)]
            x = int(record['OTP'])
            #st.write(x)
            #st.write(record['OTP'][0])
            #st.write(otp)
            if int(otp) == x:
                st.success("Verified")
                flag=1

            else:
                st.error("Wrong OTP")
with col3:
    st.write('##### Step-3: Delete Request')
    if flag==1:
        res = fetch_db({"req_id":str(req_id)})
        headers =  ["ID","App_Date", "Emp.name", "E.ID", "Designation", "Department", "Manager", "Start_Date","End_Date", "No_Days", "Reason","Work_Done_By","Leave_Type","File","Compensatory_Leave_Dates", "Status"]
        #res.columns = headers
        
        try:
            df = pd.DataFrame(res, columns= headers)
            if df.empty:
                st.error("No records found")
            else:
                #st.dataframe(df)
                x=df.to_dict()
                if x['Status'][0] == "approved":
                    
                    st.write("Your leave request was approved.")

                elif x['Status'][0] == "rejected":
                    st.write("Your leave request was rejected")
                else:
                    st.write("Your leave request is pending")
        except:
            st.error("No records available")
    else:
        pass
        #st.error("PLease verify OTP")

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