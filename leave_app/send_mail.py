import win32com.client
import streamlit as st
import pythoncom
import os
form = st.form(key="match")
with form:

    file = st.file_uploader("Upload PDF")
    if file is not None:
        st.write(file.name)
    submit = st.form_submit_button("Submit")
    if submit:
        ol=win32com.client.Dispatch("outlook.application",pythoncom.CoInitialize())
        #ol= win32com.client.Dispatch('CimplicityME.Application')
        #olmailitem=0x0 #size of the new email
        newmail=ol.CreateItem(0)
        newmail.Subject= 'Testing Mail'
        newmail.To='lokesh.skshukla@gmail.com'
        #newmail.CC='xyz@gmail.com'
        newmail.Body= 'Dear HR, <br> I have applied for leave.'
        #path = os.listdir('./')
        newfile = os.path.join(os.getcwd(), str(file.name))
        st.write(newfile)
        #attach=file.name
        newmail.Attachments.Add(newfile)
        From = None
        for myEmailAddress in ol.Session.Accounts:
            if "woxsen.edu.in" in str(myEmailAddress):
                From = myEmailAddress
                break

        if From != None:
            # This line basically calls the "mail.SendUsingAccount = xyz@email.com" outlook VBA command
            newmail._oleobj_.Invoke(*(64209, 0, 8, 0, From))
        # To display the mail before sending it
        # newmail.Display() 
        newmail.Send()

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