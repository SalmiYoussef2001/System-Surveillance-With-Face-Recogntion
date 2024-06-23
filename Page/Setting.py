import streamlit as st
from Base import Configure
if "Loggin_In" not in st.session_state:
    from Tool import Page
    Page.add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
st.set_page_config(page_title="Setting", layout="wide", initial_sidebar_state="collapsed")
# Apply custom CSS styles to hide sidebar, toolbar, and adjust other elements' styles
st.markdown('''
        <style>
            .stApp [data-testid="stToolbar"] {
                display: none;
            }
            .stApp [data-testid="stHeader"] {
                display: none;
            }
        </style>
    ''', unsafe_allow_html=True)
# Apply custom CSS to center images within the app
st.markdown('''
<style>
    .stApp [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
''', unsafe_allow_html=True)
Container = st.container().columns([0.2,0.6,0.2])[1]
CImg = Container.container(border=True)
CImg.image(f"Base/Base/Admin/{st.session_state['Profile']['name']}.jpg" )
Context = Container.container(border=True)
Name = Context.text_input("Admin User : ", value=st.session_state["Profile"]["full_name"],key="Admin-User")
E_Mail = Context.text_input("Email User : ", value=st.session_state["Profile"]["email"],key="Email-User")
Password = Context.text_input("Password User : ", type="password",value=st.session_state["Profile"]["password"],key="Password-User")
Camera_0 = Context.text_input("Camera 0 User : ", value=st.session_state["Profile"]["config"]["camera_index"][0],key="Camera-User-0")
Camera_1 =Context.text_input("Camera 1 User : ", value=st.session_state["Profile"]["config"]["camera_index"][1],key="Camera-User-1")
Base = Context.text_input("DATABASE User : ", value=st.session_state["Profile"]["config"]["database_table"],key="DATABASE-User",disabled=True)
Table = Context.text_input("Table User : ", value=st.session_state["Profile"]["config"]["table"],key="Table-User",disabled=True)
Modify = Context.columns(3)[1].button('Modify',key='Modify',use_container_width=True)
if Modify:
    Configure.modify_json(Name,E_Mail,Password,Camera_0,Camera_1)
    st.session_state["Profile"] = Configure.Return_Admin(E_Mail, Password)
    st.rerun()
Logout = Context.columns(3)[1].button('Logout',key='Logout',use_container_width=True)
if Logout :
    st.session_state['Profile'] = None
    st.session_state['DATABASE'] = None
    st.session_state['Opencv_Python'] = None
    st.session_state['Camera_0'] = None
    st.session_state['Camera_1'] = None
    st.session_state['Camera_2'] = None
    st.session_state["STATE-CAMERA-USER"] = "STOP"
    st.session_state["STATE-CAMERA-ADMIN"] = "STOP"
    st.session_state["STATE-CAMERA-FACE"] = "STOP"
    st.session_state["STATE-CAMERA-VIDEO"] = "STOP"
    st.session_state['Controlle_Pages'].delete_page("Final-PFE", "User")
    st.session_state['Controlle_Pages'].delete_page("Final-PFE", "Camera")
    st.session_state['Controlle_Pages'].delete_page("Final-PFE", "Setting")
    st.session_state["Controlle_Pages"].add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
