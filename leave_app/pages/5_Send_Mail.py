import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from time import time 
import os
#import win32com.client
#import pythoncom
from email.message import EmailMessage
import streamlit as st

st.set_page_config(
    page_title="Send Mail Tool",
    page_icon="📝",
)

st.write("# Send Mail Tool")
#ol=win32com.client.Dispatch("outlook.application",pythoncom.CoInitialize())
form = st.form(key="match")
with form:
    
    smtpsrv = "smtp.office365.com"
    smtpserver = smtplib.SMTP(smtpsrv,587)
    #msg = EmailMessage()
    body = "Dear HR, <br><br>Kindly find the attached leave application for your reference and do the needful."
    msg = MIMEMultipart()
    user = st.text_input("Your Outlook Mail ID", placeholder="Your Mail ID")
    password = st.text_input("Password", type="password")
    msg['Subject'] = 'Leave Application Form'
    #msg['Body'] = "find the attachment"
    msg['From'] = user
    msg['To'] = 'to_mail_id_separated_by_semicolon'
    msg['CC'] = 'cc_mail_id'
    msg.attach(MIMEText(body, "html"))
    file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if file is not None:
        newfilename = file.name[:-4] + str(int(time())) +".pdf"
        with open(os.path.join("temp/",newfilename),"wb") as f: 
            f.write(file.getbuffer())
        with open("temp/"+newfilename, "rb") as attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment', filename=newfilename)

            msg.attach(part)
        #st.write(newfilename)
        file = newfilename
    #msg = f"Subject: {msg['Subject']}\n\n{msg['Body']}"

    submit = st.form_submit_button("Submit")
    if submit:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(user, password)
        smtpserver.send_message (msg)
        smtpserver.close()
        st.success("Mail Sent Successfully")
        path = os.path.join('temp/', file)
        os.remove(path)

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
