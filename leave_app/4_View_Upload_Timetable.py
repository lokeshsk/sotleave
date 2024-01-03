import streamlit as st
import os
import webbrowser
import glob
from streamlit.components.v1 import html

st.header("View/Upload TimeTable")

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)


li = os.listdir("tt/")
st.write(li)
if len(li)==0:
    st.error("No timetable available to show. Kindly, ask Program Manager to upload")
#st.write(li)
else:
    for i in li:
        if i.endswith("html") and i.startswith("class"):
            #if st.button('View Class Timetable'):
            st.button('View Class TimeTable', on_click=open_page, args=('tt/class_time_table.html',),key='class')
            #webbrowser.open_new_tab("tt\\class_time_table.html")
        if i.endswith("html") and i.startswith("teachers"):
            st.button('View Teacher TimeTable', on_click=open_page, args=('tt/teachers_time_table.html',),key='teacher')
            #if st.button('View Teacher Timetable'):
             #   webbrowser.open_new_tab("tt\\teachers_time_table.html")


#url = os.path.join("temp/",newfilename)


st.markdown("""---""")
st.subheader("This section is for Program Manager(s) Only")
html_file= st.file_uploader("Upload Teacher Timetable",type=['html'])
html_file_class= st.file_uploader("Upload Class Timetable",type=['html'])
# st.write(newfilename)
if html_file is not None: 
    ext = html_file.name[-5:]
    newfilename = html_file.name[:-4]
    file = newfilename.replace(newfilename,"teachers_time_table")
    file  = file + ext
    with open(os.path.join("tt/",file),"wb") as f: 
        f.write(html_file.getbuffer())
        st.success("Succesfully uploaded teacher timetable")
else:
    pass
if html_file_class is not None: 
    ext = html_file_class.name[-5:]
    newfilename = html_file_class.name[:-4]
    file = newfilename.replace(newfilename,"class_time_table")
    file  = file + ext
    with open(os.path.join("tt/",file),"wb") as f: 
        f.write(html_file_class.getbuffer())
        st.success("Succesfully uploaded class timetable")
else:
    pass

# with st.echo():
    # st.title("dd")
    #st.markdown("[(app/static/dd.png)](https://streamlit.io)")

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