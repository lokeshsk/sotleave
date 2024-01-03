import streamlit as st
import pandas as pd
from csv import writer
st.set_page_config(
    page_title="Employee Records",
    page_icon="📝",
)

st.write("# SOT Employee Details ")
form = st.form(key="match")
with form:
    eid = st.number_input('Employee ID', min_value=170000, max_value=190000)
    e_email = st.text_input('Employee Email', placeholder ='Employee Email')
    e_email_confirm = st.text_input('Confirm E-mail ID', placeholder ='Confirm E-mail ID')
    submit = st.form_submit_button("Submit")
    if submit:
        if  eid =='' or e_email=='' or e_email_confirm =='':
            st.error("Kindly fill all the fields")
        elif e_email != e_email_confirm:
            st.error("Email and Confirm E-mail ID must be same")
        
        else:
            
            if e_email.endswith('woxsen.edu.in') and e_email_confirm.endswith('woxsen.edu.in'):
                df = pd.read_csv(r"../emp_records/emp_records.csv", header=0)
                # df = pd.read_csv('emp_records.csv')
                empid = df['E_ID'].to_list()
                empmail = df['E_EMAIL'].to_list()
                if eid in empid or e_email in empmail:
                    st.error("Record (EMp. ID/Emp. E-mail) already exists.")
                else:
                    with open(r"../emp_records/emp_records.csv", 'a', newline='') as f_object:
                    # Pass this file object to csv.writer()
                    # and get a writer object
                        List = [eid,e_email]
                        print(List)
                        writer_object = writer(f_object)
                        # Pass the list as an argument into
                        # the writerow()
                        writer_object.writerow(List)

                        # Close the file object
                        f_object.close()
                        st.success("All Information Saved Successfully")
                        eid=''
                        e_email=''
                        e_email_confirm=''
            else:
                st.error("Email ID / Confirm Mail ID must be valid woxsen e-mail id.")