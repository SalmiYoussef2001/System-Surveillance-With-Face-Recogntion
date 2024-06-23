import json
import streamlit as st
from Base import Configure
from Base.Base import MySQLDatabase
if "Loggin_In" not in st.session_state:
    from Tool import Page
    Page.add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
# Set Streamlit page configuration with title, layout, and initial sidebar state
st.set_page_config(page_title="Main", layout="centered", initial_sidebar_state="collapsed")
# Apply custom CSS styles to hide sidebar, toolbar, and adjust other elements' styles
st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
st.markdown('''
        <style>
            .stApp [data-testid="stToolbar"] {
                display: none;
            }
            .stApp [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
    ''',unsafe_allow_html=True)
st.markdown('''
<style>
    .stApp [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stApp [data-testid="stHeader"] {
        display: none;
    }
    .element-container > iframe {
        width : 1px;
        height : 1px
    }
</style>
''', unsafe_allow_html=True)

# Button to navigate back to the main page
if st.button("Back",key="Back-Main"):
    # Add and delete pages from session state to control page navigation
    st.session_state['Controlle_Pages'].add_page("Final-PFE", "streamlit_app")
    st.session_state['Controlle_Pages'].delete_page("Final", "Main")
    # Switch to the specified page
    st.switch_page("streamlit_app.py")
# Login method selection and processing
if st.session_state["Methode_Loggin_In"] == "Face":
    with st.columns([0.1,0.8,0.1])[1]:
        Face = st.camera_input("Login")
        if Face:
            # Load and process the captured face image for recognition
            Unknown = st.session_state['Face_Recognition'].load_image_file(Face)
            face_locations = st.session_state['Face_Recognition'].face_locations(Unknown)
            if len(face_locations) > 0:
                Unknown_encoding = st.session_state['Face_Recognition'].face_encodings(Unknown)[0]
                Login_UP = Configure.Face_Login(Unknown_encoding)
                if Login_UP == None:
                    st.error('Not Found Face')
                else:
                    # Set user profile and database configuration upon successful face login
                    st.session_state['Profile'] = Login_UP
                    st.session_state['DATABASE'] = MySQLDatabase('localhost',
                                                                 st.session_state['Profile']['config']['name_admin'],
                                                                 st.session_state['Profile']['config'][
                                                                     'password_database'],
                                                                 st.session_state['Profile']['config']['database_table'])
                    st.session_state['DATABASE'].connect()
                    st.session_state['DATABASE'].create_table(st.session_state['Profile']['config']['table'],
                                                              ['Id INTEGER PRIMARY KEY AUTO_INCREMENT',
                                                               'IdUser TEXT UNIQUE NOT NULL', 'Name TEXT NOT NULL',
                                                               'PathImage TEXT', 'Date TEXT', 'Role TEXT NOT NULL'])
                    # Navigate to the dashboard page
                    st.session_state["Controlle_Pages"].add_page("Final-PFE", "DashBoard")
                    st.session_state["Page_Running_State"] = "Dashboard"
                    st.session_state["Loggin_In"] = True
                    st.session_state["Controlle_Pages"].delete_page("Page", "Main")
                    st.switch_page("Page/DashBoard.py")
# Email and password login processing
if st.session_state["Methode_Loggin_In"] == "Login":
    with st.columns(3)[1]:
        Container = st.container()
        Email = Container.text_input("E-Mail",key="E-Mail-Data")
        Password = Container.text_input("Password",type="password",key="Password-Data")
        Login  = Container.button("Login",key="Button-Login",use_container_width=True)
        if Login:
            Admin_Account = Configure.Return_Admin(Email, Password)
            if Admin_Account == None:
                st.error('Invalide E-Mail And Password')
            else:
                # Set user profile and database configuration upon successful email/password login
                st.session_state['Profile'] = Admin_Account
                st.session_state['DATABASE'] = MySQLDatabase('localhost',
                                                             st.session_state['Profile']['config']['name_admin'],
                                                             st.session_state['Profile']['config'][
                                                                 'password_database'],
                                                             st.session_state['Profile']['config']['database_table'])
                st.session_state['DATABASE'].connect()
                st.session_state['DATABASE'].create_table(st.session_state['Profile']['config']['table'],
                                                          ['Id INTEGER PRIMARY KEY AUTO_INCREMENT',
                                                           'IdUser TEXT UNIQUE NOT NULL', 'Name TEXT NOT NULL',
                                                           'PathImage TEXT', 'Date TEXT', 'Role TEXT NOT NULL'])
                # Navigate to the dashboard page
                st.session_state["Controlle_Pages"].add_page("Final-PFE", "DashBoard")
                st.session_state["Page_Running_State"] = "Dashboard"
                st.session_state["Loggin_In"] = True
                st.session_state["Controlle_Pages"].delete_page("Page", "Main")
                st.switch_page("Page/DashBoard.py")
