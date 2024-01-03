import streamlit as st
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage

def leave_status_1(empar,empname,status):
    # st.write(str(empar)+" "+status)
    dfemp = pd.read_csv(r"../emp_records/emp_records.csv", header=0)
    e_s=dfemp[dfemp['E_ID']==empar]
    # st.write(e_s['E_EMAIL'])
    emp_email = e_s['E_EMAIL']
    if(emp_email.empty):
        st.write("Automated email was not sent, as your email is missing.")
    else:
        if status=='approved':
        # Define email sender and receiver
            email_sender = 'sot.leave@gmail.com'
            email_password = 'cpbo msgi jaek dywh'
            email_receiver = emp_email

            # Set the subject and body of the email
            subject = 'Leave Approved'
            body = """
            Dear {employeename},
            
            Your leave has been approved. Kindly download your leave form from 
            leave status page and send a mail to HR.

            Thank you for your patience.

            Note: This is an auto-generated mail. Kindly do not reply to this mail.

            Regards,
            SOT-APP
            """.format(employeename=empname)

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['CC']='dean.st@woxsen.edu.in'
            em['Subject'] = subject
            
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string()) 
        else:
            # Define email sender and receiver
            email_sender = 'sot.leave@gmail.com'
            email_password = 'cpbo msgi jaek dywh'
            email_receiver = emp_email

            # Set the subject and body of the email
            subject = 'Leave Rejected'
            body = """
            Dear {employeename},

            Sorry to inform you that your leave request was rejected.

            Thank you for your patience.

            Note: This is an auto-generated mail. Kindly do not reply to this mail.

            Regards,
            SOT-APP
            
            """.format(employeename=empname)

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em['CC']='dean.st@woxsen.edu.in'
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string()) 