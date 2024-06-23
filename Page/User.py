import os
from datetime import datetime
import streamlit as st
from Base import Configure
if "Loggin_In" not in st.session_state:
    from Tool import Page
    Page.add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
# Set Streamlit page configuration with title, layout, and initial sidebar state
st.set_page_config(page_title="User", layout="centered", initial_sidebar_state="collapsed")
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
# Initialize session state variables for camera settings and control
if "LIST-CANERA-ADMIN" not in st.session_state:
    # Store list of camera indexes in session state
    # st.session_state["LIST-CANERA-ADMIN"] = st.session_state["Profile"]["config"]["camera_index"]
    st.session_state["LIST-CANERA-ADMIN"]  = [0,2]
if "STATE-CAMERA-USER" not in st.session_state:
    # Initialize camera state as STOP
    st.session_state["STATE-CAMERA-USER"] = "STOP"
if "NUMBER-CAMERA-USER" not in st.session_state:
    # Initialize selected camera number
    st.session_state["NUMBER-CAMERA-USER"] = 0
if "LAST-FRAME-USER" not in st.session_state:
    # Initialize last frame captured to None
    st.session_state["LAST-FRAME-USER"] = None
if "USER-TABLE" not in st.session_state:
    # --
    st.session_state["USER-TABLE"] = st.session_state['DATABASE'].select_records(st.session_state['Profile']['config']['table'])
if "TABLE-FACE-NAME" not in st.session_state:
    st.session_state["TABLE-FACE-NAME"] = []
    for User in st.session_state["USER-TABLE"]:
        st.session_state["TABLE-FACE-NAME"].append(User[2])
if "TABLE-FACE-ENCODING" not in st.session_state:
    st.session_state["TABLE-FACE-ENCODING"] = []
    for User in st.session_state["USER-TABLE"]:
        known_face_image = st.session_state['Face_Recognition'].load_image_file(User[3])
        known_face_encoding = st.session_state['Face_Recognition'].face_encodings(known_face_image)[0]
        st.session_state["TABLE-FACE-ENCODING"].append(known_face_encoding)
# st.write(st.session_state)
# Camera control UI when camera is stopped
if st.session_state["STATE-CAMERA-USER"] == "STOP":
    Container = st.container(border=True)
    # Number input for selecting camera
    st.session_state["NUMBER-CAMERA-USER"] = Container.number_input("Number : ", min_value=0, max_value=100, value=0)
    # Start button to initiate camera feed
    START = Container.columns(3)[1].button("Start", key="Start-User", use_container_width=True)
    with Container.columns([0.2,0.6,0.2])[1]:
        Context = st.container(border=True)
        # Display last frame if available
        if st.session_state["LAST-FRAME-USER"] is not None:
            Context.image(st.session_state["LAST-FRAME-USER"], channels="BGR", use_column_width=True)
            NUMBER_FACES = st.session_state['Face_Recognition'].face_locations(st.session_state["LAST-FRAME-USER"])
            if 0 < len(NUMBER_FACES) < 2:
                Unknown_encoding = st.session_state['Face_Recognition'].face_encodings(st.session_state["LAST-FRAME-USER"])[0]
                User, Len = Configure.Search_USER(st.session_state['Profile']['config']['table'], Unknown_encoding,st.session_state['Profile']['config']['table'])
                if User is None:
                    Context = st.container(border=True)
                    Context.markdown("<center> ADD USER </center>", unsafe_allow_html=True)
                    Context.text_input("new Name User : ", value="", key="NEW-NAME-USER")
                    Context.radio("Enter Role User", ["Admin", "User"], horizontal=True, key="NEW-ROLE-USER",index=1)
                    ADD = Context.button("ADD", key="ADD-USER",use_container_width=True)
                    if ADD:
                        current_time = datetime.now().strftime('%H:%M')
                        current_date = datetime.now().strftime('%Y/%m/%d')
                        Data_ADD = current_date + ' ' + current_time
                        # st.session_state['DATABASE'].delete_record(st.session_state['Profile']['config']['table'], f'IdUser = \'User0\'')
                        st.session_state['DATABASE'].insert_record(st.session_state['Profile']['config']['table'],
                                                                   {'IdUser': f'User{Len}',
                                                                    'Name': st.session_state['NEW-NAME-USER'],
                                                                    'PathImage': f"Base/Data/{st.session_state['Profile']['config']['table']}/Faces/User{Len}.png",
                                                                    'Date': Data_ADD,
                                                                    'Role': st.session_state['NEW-ROLE-USER']})
                        Configure.ADD_Face(st.session_state['Profile']['config']['table'], Unknown_encoding.tolist())
                        output_folder = f"Base/Data/{st.session_state['Profile']['config']['table']}/Faces"
                        frame_filename = os.path.join(output_folder, f"User{Len}.png")
                        st.session_state['Opencv_Python'].imwrite(frame_filename,st.session_state["LAST-FRAME-USER"])
                        st.session_state["USER-TABLE"] = st.session_state['DATABASE'].select_records(st.session_state['Profile']['config']['table'])
                        st.session_state["TABLE-FACE-NAME"] = []
                        for User in st.session_state["USER-TABLE"]:
                            st.session_state["TABLE-FACE-NAME"].append(User[2])
                        st.session_state["TABLE-FACE-ENCODING"] = []
                        for User in st.session_state["USER-TABLE"]:
                            known_face_image = st.session_state['Face_Recognition'].load_image_file(User[3])
                            known_face_encoding = st.session_state['Face_Recognition'].face_encodings(known_face_image)[0]
                            st.session_state["TABLE-FACE-ENCODING"].append(known_face_encoding)
                        st.rerun()
                else:
                    User = Len['ID_User']
                    Users = st.session_state['DATABASE'].select_records(st.session_state['Profile']['config']['table'], f'IdUser = \'{User}\'')
                    with st.form("CHANGE-USER",border=True):
                        Context = st.container(border=True)
                        Context.markdown("<center> Change Info USER </center>", unsafe_allow_html=True)
                        Name = Context.text_input("new Name User : ", value=Users[0][2], key="NEW-NAME-USER")
                        if Users[0][5] == "Admin":
                            Role = Context.radio("Enter Role User", ["Admin", "User"], horizontal=True, key="NEW-ROLE-USER-0",index=0)
                        else:
                            Role = Context.radio("Enter Role User", ["Admin", "User"], horizontal=True, key="NEW-ROLE-USER-1",index=1)
                        CHANGE = st.form_submit_button("Change", use_container_width=True)
                    if CHANGE:
                        # Update the record with IdUser == User2
                        condition = f"IdUser = '{Users[0][1]}'"
                        data = {"Name": Name, "Role": Role}
                        st.session_state['DATABASE'].update_record(
                            table_name=st.session_state['Profile']['config']['table']
                            , data=data, condition=condition)
                        st.session_state['SEARCH_BY_NAME'] = False
                        st.toast("OK")
                        st.rerun()
    # Change state to START when button is pressed
    if START:
        st.session_state["STATE-CAMERA-USER"] = "START"
        st.rerun()
# Camera control UI when camera is started
if st.session_state["STATE-CAMERA-USER"] == "START":
    Container = st.container(border=True)
    # Stop button to halt camera feed
    STOP = Container.columns(3)[1].button("Stop", key="Stop-User", use_container_width=True)
    LIVE = Container.empty()
    # Initialize camera with selected index
    CAMERA = st.session_state['Opencv_Python'].VideoCapture(st.session_state["LIST-CANERA-ADMIN"][st.session_state["NUMBER-CAMERA-USER"]])
    # Read and display frames from the camera
    while CAMERA.isOpened() and not STOP:
        Ret, Frame = CAMERA.read()
        if not Ret or Frame is None:
            # Release camera if frame is not received
            CAMERA.release()
            break
        if Frame is not None:
            # Display current frame
            LIVE.image(Frame, channels="BGR")
            # Store current frame as last frame
            st.session_state["LAST-FRAME-USER"] = Frame.copy()
    # Change state to STOP when button is pressed
    if STOP:
        st.session_state["STATE-CAMERA-USER"] = "STOP"
        st.rerun()
