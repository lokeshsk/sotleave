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
    page_title="Delete Leave Request",
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

# Add SSL (layer of security)
context = ssl.create_default_context()
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
        if x['Status'][0] == "pending":
            empname = x['Emp.name'][0]
            empar = x['E.ID'][0]
            dfemp = pd.read_csv(r"../emp_records/emp_records.csv", header=0)
            e_s=dfemp[dfemp['E_ID']==empar]
            # st.write(e_s['E_EMAIL'])
            emp_email = e_s['E_EMAIL']
            if(emp_email.empty):
                st.write("Automated email was not sent, as your email is missing.")
            else:
                df2 = pd.read_csv("otp_del.csv")
                df2 = df2.astype('str')
                df2['OTP']= df2['OTP'].str.replace(',','',regex=True)
                record2 = df2[df2['REQ_ID']==str(req_id)]
                x = int(record2['OTP'])
                #x = record2['OTP'].astype(int)
                email_sender = 'your_mail'
                email_password = 'your_pass'
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

                

                # Log in and send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string()) 

                    st.success("OTP sent successfully to your mail id.")


        elif x['Status'][0] == "approved":
            st.error("As your leave request was approved, the leave request cannot be deleted. Only pending leave requests can be deleted.")
        else:
            st.error("As your leave request was rejected, the leave request cannot be deleted. Only pending leave requests can be deleted.")
    

col1, col2,col3 = st.columns(3)

global flag
flag=0
with col1:
    st.write('##### Step-1: Generate OTP')
    with st.form(key='Form1'):
        req_id = st.text_input('Request ID',placeholder="Request ID")
        submit = st.form_submit_button("Generate OTP", type='primary')   
        if submit:
            try:
                ver_otp = random_with_N_digits(6)
                df1 = pd.read_csv("otp_del.csv")
                record1 = df1['REQ_ID'].to_list()
                list_int = map(int, record1)
                if req_id=='':
                    st.error("Request id cannot be empty")
                elif req_id.isnumeric()==False:
                    st.error("Request id must be a number")
                
                elif int(req_id) not in record1:
                    f = open("otp_del.csv","a", newline='')
                    csvwriter = csv.writer(f) 
                    fields=[req_id,ver_otp]
                    csvwriter.writerow(fields)  
                    f.close()
                    send_email()
                    #st.write(ver_otp)
                else:
                    send_email()
            except: 
                st.error("Invalid request ID")
        #if st.button("Verify"):
        #verify()
        
                #verify()
with col2:
    st.write('##### Step-2: Verify OTP')
    with st.form('Form2'):
        otp = st.text_input('Enter OTP',placeholder="OTP")
        submit = st.form_submit_button("Verify and Delete", type='primary')
        if submit:
            if otp=='':
                st.error("OTP cannot be blank")
            elif req_id=='':
                st.error("Kindy, generate OTP using your Request ID")

            else:
                if req_id.isnumeric()==False:
                    st.error("Request id must be a number")
                else:
                    try:
                        otp = int(otp)
                        df = pd.read_csv("otp.csv")
                        df = df.astype('str')
                        df['OTP']= df['OTP'].str.replace(',','',regex=True)
                        record = df[df['REQ_ID']==str(req_id)]
                        x = record['OTP'].astype(int)
                        if x.empty:
                            st.error("Invalid Request ID")
                        elif otp == x.iloc[0]:
                            st.success("Verified")
                            flag=1
                        else:
                            st.error("Wrong OTP")
                    except:
                        st.error("OTP must be numeric")
with col3:
    st.write('##### Step-3: Delete Request')
    # st.write(flag)
    if flag==1:
        #with st.form(key='Form3'):
        # st.write(flag)
        res2 = fetch_db({"req_id":str(req_id)})
        headers =  ["ID","App_Date", "Emp.name", "E.ID", "Designation", "Department", "Manager", "Start_Date","End_Date", "No_Days", "Reason","Work_Done_By","Leave_Type","File","Compensatory_Leave_Dates", "Status"]
        # st.write(res[0][1])
        df = pd.DataFrame(res2, columns= headers)
        st.write("We found the following record:")
        st.write(df)
        sql_del = "DELETE FROM leave_records WHERE ID = %s"
        val = req_id
        mycursor.execute(sql_del,(val,))
        mydb.commit()
        if req_id=='':
            col3.title('No records to delete')
            st.error("No records to delete")
        else:
            #col3.title("Record of leave request id "+req_id+" deleted successfully.")
            st.success("Record of leave request id "+req_id+" deleted successfully.")
    else:
        pass
        # st.error("Your OTP was not verified")
            


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
