# Initialization Library
import streamlit as st
if "Loggin_In" not in st.session_state:
    from Tool import Page
    Page.add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
# Set the configuration for the Streamlit page including the title, layout, and initial sidebar state
st.set_page_config(page_title="Main", layout="centered", initial_sidebar_state="collapsed")
# Apply custom CSS styles to hide the sidebar when expanded, remove the Streamlit toolbar, and adjust other UI elements
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

# Create a back button to navigate to a previous page and update session state accordingly
if st.button("Back",key="Back-App"):
    st.session_state['Controlle_Pages'].add_page("Final-PFE", "streamlit_app")
    st.session_state['Controlle_Pages'].delete_page("Final", "App")
    st.switch_page("streamlit_app.py")
    
# Display different UI elements based on the window width to enhance responsiveness
if st.session_state["Window-InnerWidth"] > 700 :
    with st.columns(3)[1]:
        Container = st.container(border=True)
        Container.image("Icon/Logo.png" ,width=90)
        Face   = Container.button("Face",key="Face",use_container_width=True)
        Login  = Container.button("Login",key="Login",use_container_width=True)
else:
    with st.columns(3)[1]:
        Container = st.container(border=True)
        Container.image("Icon/Logo.png", width=90)
        Face = False
        Login  = Container.button("Login", key="Login", use_container_width=True)

# Handle navigation and session state updates based on user interaction with the Face and Logi buttons
if Face:
    st.session_state['Controlle_Pages'].add_page("Final", "Main")
    st.session_state['Controlle_Pages'].delete_page("Final", "App")
    st.session_state["Methode_Loggin_In"] = "Face"
    st.switch_page("Page/Main.py")
if Login:
    st.session_state['Controlle_Pages'].add_page("Final", "Main")
    st.session_state['Controlle_Pages'].delete_page("Final", "App")
    st.session_state["Methode_Loggin_In"] = "Login"
    st.switch_page("Page/Main.py")
