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

st.write("# Check Leave Status")

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

def download(f):
    with open(f, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(label="Download PDF",
                        data=PDFbyte,
                        file_name=f,
                        mime='application/octet-stream')

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



def create_pdf(datap: dict):
    today = date.today()
    sdate = datetime.strptime(str(datap['sdate']), "%Y-%m-%d").strftime("%d-%m-%Y")
    edate = datetime.strptime(str(datap['edate']), "%Y-%m-%d").strftime("%d-%m-%Y")
    doa = datetime.strptime(str(datap['doa']), "%Y-%m-%d").strftime("%d-%m-%Y")
    today = datetime.strptime(str(today), "%Y-%m-%d").strftime("%d-%m-%Y")
    
    canvas = Canvas("leave_approved_"+str(datap['eid'])+".pdf", pagesize=LETTER)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(black)
    t0 = f"LEAVE APPLICATION FORM"
    canvas.drawString(190, 680,  t0)
    canvas.line(90,670,550,670)
    canvas.setFont("Helvetica", 12)
    t1 = f"Date of Application: {doa}"
    canvas.drawString(90, 640,  t1)
    t2 = f"Employee Name: {datap['ename']}"  
    canvas.drawString(90, 610,  t2)
    t3 = f"Employee ID: {datap['eid']}"
    canvas.drawString(90, 580,  t3)
    t4 = f"Designation: {datap['des']}"
    canvas.drawString(90, 550,  t4)
    t5 = f"Department: {datap['dep']}"
    canvas.drawString(90, 520,  t5)
    t6 = f"Manager: {datap['man']}"
    canvas.drawString(90, 490,  t6)
    
    t7 = f"Leave Start Date: {sdate}"
    canvas.drawString(90, 460,  t7)
    t8 = f"Leave End Date: {edate}"
    canvas.drawString(90, 430,  t8)
    t9 = f"Number of days of leave: {datap['nodays']}"
    canvas.drawString(90, 400,  t9)
    t10 = f"Reason For Leave: {datap['reason']}"
    canvas.drawString(90, 370,  t10)
    t11 = f"Work Done By: {datap['work']}"
    canvas.drawString(90, 340,  t11)    
    t12 = f"Nature Of Leave: {datap['ltype']}"
    canvas.drawString(90, 310,  t12) 
    t19 = f"Compensatory Leave Dates: {datap['cleaves']}"
    canvas.drawString(90, 280,  t19)    
    t13 = f"Manager Approval: {datap['status']}"
    canvas.drawString(90, 250,  t13)
    #t14 = f"Employee Signature: {datap['file']}"
    #canvas.drawString(90, 310,  t14)
    canvas.drawImage("uploads/"+str(datap['file']), 90, 170, width=120, height = 60, preserveAspectRatio=True, mask='auto')
    t15 = f"Employee Signature"
    canvas.drawString(90, 150,  t15)
    t17 = f"Date: {doa}"
    canvas.drawString(90, 130,  t17)
    canvas.drawImage("temp/dd.png", 450, 170, width=120, height=60, preserveAspectRatio=True, mask='auto')
    t16 = f"Manager Signature"
    canvas.drawString(450, 150,  t16)
    t18 = f"Date: {today}"
    canvas.drawString(450, 130,  t18)
    canvas.drawImage("uploads/logo.png", 450, 615, width=100,preserveAspectRatio=True, mask='auto')
    canvas.save()
    return "leave_approved_"+str(datap['eid'])+".pdf"


# Add SSL (layer of security)
context = ssl.create_default_context()
#with form:
pdffile=''
#req_id = st.text_input('Enter Request ID', placeholder ='Enter Request ID')
st.divider()
def send_email():
    #ui.notify("")
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
                #x = record2['OTP'].astype(int)
                email_sender = 'your_mail'
                email_password = 'your_pass'
                email_receiver = emp_email

                # Set the subject and body of the email
                subject = 'OTP - SOT Leave APP'
                body = """
                Dear {employeename},
                
                Your OTP to download PDF is {x}.

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
            if req_id=='':
                st.error("Request ID cannot be blank")

            else:
                try:
                    req_id = int(req_id)
                    ver_otp = random_with_N_digits(6)
                    df1 = pd.read_csv("otp.csv")
                    record1 = df1['REQ_ID'].to_list()
                    list_int = map(int, record1) 
                    #st.write(list_int)
                    
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
                except:
                    st.error("Request ID must be numeric")
                
            #if st.button("Verify"):
        #verify()
        
                #verify()
with col2:
    st.write('##### Step-2: Verify OTP')
    with st.form('Form2'):
        otp = st.text_input('Enter OTP',placeholder="OTP")
        submit = st.form_submit_button("Verify OTP", type='primary')
        if submit:
            if otp=='':
                st.error("OTP cannot be blank")
            elif req_id=='':
                st.error("Kindy, generate OTP using your Request ID")

            else:
                try:
                    otp = int(otp)
                    df = pd.read_csv("otp.csv")
                    df = df.astype('str')
                    df['OTP']= df['OTP'].str.replace(',','',regex=True)
                    record = df[df['REQ_ID']==str(req_id)]

                    x = int(record['OTP'])
                    #x = record['OTP'].astype(int)
                    #st.write(x)
                    #st.write(record['OTP'][0])
                    #st.write(otp)
                    if int(otp) == x:
                        st.success("Verified")
                        flag=1

                    else:
                        st.error("Wrong OTP")
                except:
                    st.error("OTP must be numeric")

with col3:
    st.write('##### Step-3: Download-PDF')
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
                    pdffile = create_pdf(
                    {"doa":x['App_Date'][0],
                    "ename":x['Emp.name'][0],
                    "eid":x['E.ID'][0],
                    "des":x['Designation'][0],
                    "dep":x['Department'][0],
                    "man":x['Manager'][0],
                    "sdate":x['Start_Date'][0],
                    "edate":x['End_Date'][0],
                    "nodays":x['No_Days'][0],
                    "reason":x['Reason'][0],
                    "work":x['Work_Done_By'][0],
                    "ltype":x['Leave_Type'][0],
                    "cleaves":x['Compensatory_Leave_Dates'][0],
                    "status":x['Status'][0],
                    "file":x['File'][0]}   
                    )
                    
                    st.write("Your leave request was approved. PDF Created Successfully")
                    try:
                        download(pdffile)
                    except:
                        pass
                elif x['Status'][0] == "rejected":
                    st.write("Your leave request was rejected")
                else:
                    st.write("Your leave request is pending")
        except:
            st.error("No records available")
    else:
        pass
        #st.error("PLease verify OTP")
# with col2:
#     with st.form('Form2'):
#         otp = st.text_input('Enter OTP',placeholder="OTP")
#         submit = st.form_submit_button("Verify OTP", type='primary')
#         if submit:

#             df = pd.read_csv("otp.csv")
#             record = df[df['REQ_ID']==req_id]
#             st.write(record['OTP'])
#             if str(otp) == str(record['OTP']):
#                 st.sucess("hello")
#             else:
#                 st.error("bye")
#submit = st.form_submit_button("Generate OTP", type='primary')
#if submit:


# ver_otp = ''
# with form:
#     req_id = st.text_input('Request ID',placeholder="Request ID")
#     submit = st.form_submit_button("Generate OTP", type='primary')
# if submit:
#     if req_id=='' or  req_id.isnumeric()==False:
#         st.error("error")
#     else:
#         ver_otp = random_with_N_digits(6)
#         df1 = pd.read_csv("otp.csv")
#         record1 = df1['REQ_ID'].to_list()
        
#         st.write(record1)
#         if req_id not in record1:
#             f = open("otp.csv","a", newline='')
#             csvwriter = csv.writer(f) 
#             fields=[req_id,ver_otp]
#             csvwriter.writerow(fields)  
#             f.close()
#             st.write(ver_otp)
#         else:
#             pass
        
#         verify()




# if st.button("Verify"):
#     if otp == ver_otp:
#         st.write("hello")
#     else:
#         st.write("bye")


    # st.write("Your Request is in process.")
     

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
