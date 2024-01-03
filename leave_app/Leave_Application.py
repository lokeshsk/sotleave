import streamlit as st
from datetime import date
#from fpdf import FPDF
import base64
import mysql.connector
import os
from PIL import Image
from time import time 
import datetime
import pandas as pd
#import pywhatkit as py
from random import randint
import csv
from email.message import EmailMessage
import smtplib
import ssl

now = datetime.datetime.now()


st.set_page_config(
    page_title="Leave Application",
    page_icon="📝",
)
#st.sidebar.success("Apply / ChecK Leave Status")

def load_image(image_file):
    img = Image.open(image_file)
    return img

def db_connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="leaves"
    )
    return mydb


leave_nature=''
cleaves_date=''

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def send_email():
    context = ssl.create_default_context()
    empname = ename
    empar = eid
    dfemp = pd.read_csv(r"../emp_records/emp_records.csv", header=0)
    dfemp['E_ID'] = dfemp['E_ID'].astype(str)
    dfemp['E_ID'] = dfemp['E_ID'].replace(",", "") 
    #st.write(dfemp)
    e_s=dfemp[dfemp['E_ID']==empar]
    #st.write(e_s['E_EMAIL'])
    emp_email = e_s['E_EMAIL']
    if(emp_email.empty):
        st.write("Automated email was not sent, as your email is missing.")
    else:
        df2 = pd.read_csv("otp_apply.csv")
        df2 = df2.astype('str')
        df2['OTP']= df2['OTP'].str.replace(',','',regex=True)
        record2 = df2[df2['E_ID']==str(eid)]
        x1 = int(record2['OTP'])
        #x1 = record2['OTP'].astype(int)
        email_sender = 'sot.leave@gmail.com'
        email_password = 'cpbo msgi jaek dywh'
        email_receiver = emp_email

        # Set the subject and body of the email
        subject = 'OTP For Leave Application- SOT Leave APP'
        body = """
        Dear {employeename},
        
        Your OTP to apply for leave is {x1}.

        Note: This is an auto-generated mail. Kindly do not reply to this mail.

        Regards,
        SOT-APP
        """.format(employeename=empname, x1 = x1)

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

def store_in_db(data: dict):
    #st.write(data)
    #st.write(data[0])
    #st.write(type(data[0]))
    mydb = db_connect()
    mycursor = mydb.cursor()
    qry = "Insert Into leave_records (app_date, ename, eid, designation, department, manager, start_date, end_date, no_days, reason, work_done, nature, esign, status, cleaves ) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (data['doa'],data['ename'],data['eid'],data['designation'],data['department'],data['manager'],data['start_date'],data['end_date'],data['no_days'],data['reason'],data['work_done'],data['leave_nature'],data['file_name'],data['status'],data['cleaves'])
    mycursor.execute(qry, val)
    mydb.commit()
    return mycursor.lastrowid

def fetch_db(eid):
    #st.write(data)
    mydb2 = db_connect()
    mycursor2 = mydb2.cursor()
    qry = "select start_date, end_date, no_days  from leave_records where eid = %s and status = %s "
    #val = (data['req_id'],)
    mycursor2.execute(qry,[eid,'pending'])
    res2 = mycursor2.fetchall()
    return res2
i=1
st.write("# SOT Leave Application Portal ")
form = st.form(key="match")
with form:
    #doa = st.date_input("Date of Application", min_value = date.today(),disabled=True)
    doa = st.date_input("Date of Application", min_value = date.today(),disabled=True)
    ename = st.text_input('Employee Name', placeholder ='Employee Name')
    eid = st.text_input('Employee ID', placeholder="Employee ID")
    #int_val = st.number_input('Seconds', min_value=1, max_value=10, value=5, step=1)
    designation = st.text_input('Designation', placeholder ='Designation')
    department = st.text_input('Department', placeholder ='Department', value="School of Technology", disabled=True)
    #st.caption(':black[**Manager**]')
    manager = st.text_input("Manager", placeholder = "Manager Name", value="Dr. Kiran K Ravulakollu", disabled=True)
    #start_date = st.date_input("Leave Start Date", min_value = date.today())
    start_date = st.date_input("Leave Start Date")
    #end_date = st.date_input("Leave End Date", min_value = date.today())
    end_date = st.date_input("Leave End Date")
    #st.caption(':black[**No. of Days**]')
    days = abs(end_date - start_date )
    #days = str(int(str(days)) +1)
    no_days = st.text_input("No. of Days" ,placeholder="No. of Days")
    # size = len(days)
    # # Slice string to remove last 3 characters from string
    # days = days[:size - 9]
    # no_days = st.write(days)
    reason = st.text_input('Reason for leave', placeholder = 'Reason for leave')
    work_done = st.text_input('In absence work will be done by', placeholder = 'In absence work will be done by')
    placeholder_for_selectbox = st.empty()
    placeholder_for_optional_text = st.empty()
    #ephone = st.text_input('Phone number without country code (will be used only for leave status update)', placeholder='Mobile number which is linked to WhatsApp',max_chars=10)
    image_file = st.file_uploader("Upload Your Sign",type=['png','jpeg','jpg'])
    # if image_file is not None:
        # file_details = {"FileName":image_file.name,"FileType":image_file.type}
        # st.write(file_details)
        # img = load_image(image_file)
        # st.image(img)
    # else:
        # pass
    submit = st.form_submit_button("Generate OTP")

# Create selectbox
with placeholder_for_selectbox:
    options = ['Sick Leave', 'Earned Leave','On Duty', 'Leave Without Pay'] + ["Compensatory Leave"]
    leave_nature = st.selectbox("Nature of Leave", options=options)

# st.info(leave_nature)
# Create text input for user entry
with placeholder_for_optional_text:
    if leave_nature == "Compensatory Leave":
        cleaves_date = st.text_input("Enter compensatory dates (use comma for multiple dates)",placeholder="Enter in dd-mm-yyyy format")
    else:
        cleaves_date = "Not Applicable"
        
if submit:
    try:
        no_days=float(no_days)
    except:
        st.error("No. of Days must be in Numbers only. Hint: For Half Day Leave, use 0.5")
        st.stop()
    if doa=='' or ename=='' or eid =='' or designation=='' or department=='' or manager=='' or start_date=='' or end_date=='' or no_days=='' or reason=='' or work_done=='' or leave_nature=='' or image_file==None:
        st.error("Kindly fill all the fields")
    elif eid.isnumeric()==False:
        st.error("Employee ID must be Numbers")
    elif start_date > end_date:
        st.error("Start Date cannot be greater than End Date.")
    # elif isinstance(no_days, str) ==True:
    #     #st.write(type(no_days))
    #     st.error("No. of Days must be in Numbers only. Hint: For Half Day Leave, use 0.5")
    else:
        
        
        df = pd.read_csv(r"../emp_records/emp_records.csv")
        # df = pd.read_csv("../manager_login/emp_records.csv")
        #eid_data = df['E_ID'].to_list()
        ver_otp = random_with_N_digits(6)
        df1 = pd.read_csv("otp_apply.csv")
        
        record1 = df1['E_ID'].to_list()
        list_int = map(int, record1) 
        #st.write(record1)
        if int(eid) not in record1:
            f = open("otp_apply.csv","a", newline='')
            csvwriter = csv.writer(f) 
            fields=[eid,ver_otp]
            csvwriter.writerow(fields)  
            f.close()
            #st.write(ver_otp)
            send_email()
            
        else:
            #st.write("in else")
            send_email()

        #st.success("Submitted Request Succesfully")
        
        if int(eid) in df["E_ID"].values:
            pass
        else:
            st.error("Your e-mail is missing in records. Kindly update using ADD EMPLOYEE RECORDS option given in the menu.")


with st.form(key="verify"):
    otp = st.text_input('Enter OTP', placeholder ='Enter OTP')
    submit = st.form_submit_button("Submit", type="primary")
    if submit:
        if otp=='':
                st.error("OTP cannot be blank")
        elif eid=='':
            st.error("Kindy, generate OTP using your EMP. ID")

        else:
            try:
                otp = int(otp)
                df = pd.read_csv("otp_apply.csv")
                df = df.astype('str')
                df['OTP']= df['OTP'].str.replace(',','',regex=True)
                record = df[df['E_ID']==str(eid)]
                
                #x = int(record['OTP'])
                #st.write(record)
                x = record['OTP'].astype(int)
                #st.write(type(x))
                if x.empty:
                    st.error("Invalid Request ID")
                elif otp == x.iloc[0]:
                    ext = image_file.name[-4:]
                    newfilename = image_file.name[:-4] + str(int(time())) +ext
                    req_exists = pd.DataFrame(fetch_db(eid))
                    #st.dataframe(req_exists)
                    if req_exists.empty:
                        rid = store_in_db({"doa":str(doa),"ename":ename,"eid": eid, "designation":designation,"department": department, "manager":manager, "start_date":str(start_date),"end_date": str(end_date), "no_days":str(no_days),"reason": reason, "work_done":work_done, "leave_nature":leave_nature, "file_name":newfilename,"status":"pending","cleaves":cleaves_date})
                        with open(os.path.join("uploads/",newfilename),"wb") as f: 
                            f.write(image_file.getbuffer())
                        st.subheader("Kindly, note down your Request ID: **"+str(rid)+"**")
                        st.success("Application Submitted Successfully")
                    else:
                        req_exists = req_exists.astype('str')
                        st_dt = req_exists[0].to_list()
                        en_dt = req_exists[1].to_list()
                        nod = req_exists[2].to_list()

                        if str(start_date) in str(st_dt) and str(end_date) in str(en_dt) and str(no_days) in str(nod):
                            #st.write(start_date)
                            #st.write(st_dt)

                            st.error("Record already exists, for same dates.")
                        else:
                            rid = store_in_db({"doa":str(doa),"ename":ename,"eid": eid, "designation":designation,"department": department, "manager":manager, "start_date":str(start_date),"end_date": str(end_date), "no_days":str(no_days),"reason": reason, "work_done":work_done, "leave_nature":leave_nature, "file_name":newfilename,"status":"pending","cleaves":cleaves_date})
                            with open(os.path.join("uploads/",newfilename),"wb") as f: 
                                f.write(image_file.getbuffer())
                            st.subheader("Kindly, note down your Request ID: **"+str(rid)+"**")
                            st.success("Application Submitted Successfully")


                else:
                    st.error("Wrong OTP")
            except Exception as e:
                st.write(e)
                st.error("OTP must be numeric")
        # st.success("Submitted Request Succesfully")
        # st.subheader("Kindly, note down your Request ID: **"+str(rid)+"**")
            # phonelist = '9000569938'
            # phone = phonelist.split(',')
            # message = "Leave application submitted successfully by "+ename+" on "+str(date.today()) +" with following reason: "+reason
            # for each in phone:
                # py.sendwhatmsg_instantly("+91"+each,message,now.hour,(now.minute+i),10)
                # i=i+1
                # st.success("Message Sent!")

# export_as_pdf = st.button("Export Leave Form")
# def create_download_link(val, filename):
#     b64 = base64.b64encode(val)  # val looks like b'...'
#     return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

# if export_as_pdf:
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 16)
#     pdf.cell(40, 10, str(doa))
#     pdf.cell(40, 20, ename)
#     pdf.cell(40, 30, eid)
#     pdf.cell(100, 10, designation)
#     #pdf.cell(40, 90, esign)
#     html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

#     st.markdown(html, unsafe_allow_html=True)



# with conn.session as s:
#     s.execute(
#             'INSERT INTO leave_records (app_date, ename) VALUES (:app_date, :ename);',
#             params=dict(app_date=doa, ename = ename))
#     s.commit()
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
