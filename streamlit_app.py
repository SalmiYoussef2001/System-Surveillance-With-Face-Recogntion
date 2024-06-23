# Initialization Library
import streamlit as st
from streamlit_javascript import st_javascript
st.set_page_config(page_title="Main", layout="centered", initial_sidebar_state="collapsed")
# this line for after logout admin with clear cache
if 'Controlle_Pages' in st.session_state:
    # -------------------------------------------------------------------------------
    st.session_state['Controlle_Pages'].delete_page("Final", "Setting")
# Initialization style page
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
# Initialization function cache resource
@st.cache_resource
def Initialization_Streamlit_Components():
    """
    Initializes and caches the Streamlit components module.

    Returns:
        module: The Streamlit components module.
    """
    import streamlit.components.v1
    return streamlit.components.v1
@st.cache_resource
def Initialization_Face_Recognition():
    """
    Initializes and caches the face recognition module.

    Returns:
        module: The face recognition module.
    """
    import face_recognition
    return face_recognition
@st.cache_resource
def Initialization_Opencv_Python():
    """
    Initializes and caches the OpenCV module.

    Returns:
        module: The OpenCV module.
    """
    import cv2
    return cv2
@st.cache_resource
def Initialization_ADD_DELET_Page():
    import Tool.Page
    return Tool.Page
# Initialization session state
st.session_state["Page_Running_State"] = "Streamlit_App"
st.session_state["Loggin_In"] = False
st.session_state["Profile"] = None
st.session_state["DATABASE"] = None
st.session_state["Methode_Loggin_In"] = None
st.session_state['Face_Recognition'] = Initialization_Face_Recognition()
st.session_state['Streamlit_Components'] = Initialization_Streamlit_Components()
st.session_state['Opencv_Python'] = Initialization_Opencv_Python()
st.session_state['Controlle_Pages'] = Initialization_ADD_DELET_Page()
st.session_state['SEARCH_BY_NAME'] = False
st.markdown("<center> <h1> System Security </h1> </center>",unsafe_allow_html=True)
Width = st_javascript("""screen.width;""")
with st.columns(3)[1]:
    st.image("Icon/Logo.png",width=90)
    if st.button("Welecome",use_container_width=True):
        st.session_state['Controlle_Pages'].add_page("Final-PFE", "App")
        st.session_state['Controlle_Pages'].delete_page("Final-PFE", "streamlit_app")
        st.session_state["Window-InnerWidth"] = Width
        st.switch_page("Page/App.py")
