import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
from Base import Configure
if "Loggin_In" not in st.session_state:
    from Tool import Page
    Page.add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
st.set_page_config(page_title="Camera", layout="wide", initial_sidebar_state="collapsed")
if "LIST-CAMERA" not in st.session_state:
    st.session_state["LIST-CAMERA"] = [None, None]
if "COPY-LIST-CAMERA" not in st.session_state:
    st.session_state["COPY-LIST-CAMERA"] = [None, None]
if 'STOP' not in st.session_state:
    st.session_state['STOP'] = False
if 'BUTTON-CAMERA' not in st.session_state:
    st.session_state['BUTTON-CAMERA'] = 'STOP'
if "USER-TABLE" not in st.session_state:
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
st.markdown('''
<style>
    .stApp [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
''', unsafe_allow_html=True)
@st.cache_resource
def VideoCapture_Camera_0():
    # return st.session_state['Opencv_Python'].VideoCapture("http://127.0.0.1:5001/livestream?camera=2")
    # return st.session_state['Opencv_Python'].VideoCapture(0)
    return st.session_state['Opencv_Python'].VideoCapture(int(st.session_state["Profile"]["config"]["camera_index"][0]))
@st.cache_resource
def VideoCapture_Camera_1():
    # return st.session_state['Opencv_Python'].VideoCapture("http://127.0.0.1:5000/livestream?camera=0")
    # return st.session_state['Opencv_Python'].VideoCapture(2)
    return st.session_state['Opencv_Python'].VideoCapture(int(st.session_state["Profile"]["config"]["camera_index"][1]))
Title = st.empty()
Container = st.container()
BUTTON = Container.button(st.session_state['BUTTON-CAMERA'], key="Start", use_container_width=True)
Cols = Container.columns(2)
VIDEO_0 = Cols[0].empty()
VIDEO_1 = Cols[1].empty()
if BUTTON:
    if st.session_state['BUTTON-CAMERA'] == 'STOP':
        st.session_state['STOP'] = True
        VideoCapture_Camera_0.clear()
        VideoCapture_Camera_1.clear()
        st.session_state["LIST-CAMERA"][0] = None
        st.session_state["LIST-CAMERA"][1] = None
        st.session_state['BUTTON-CAMERA'] = 'START'
    else:
        st.session_state['BUTTON-CAMERA'] = 'STOP'
        st.session_state["LIST-CAMERA"][0] = VideoCapture_Camera_0()
        st.session_state["LIST-CAMERA"][1] = VideoCapture_Camera_1()
        st.session_state['STOP'] = False
    st.rerun()
# Title.write(st.session_state)
PROCESS_THIS_FRAME = True
Face_Locations_0 = []
Face_Encodings_0 = []
Face_Names_0 = []
Face_Locations_1 = []
Face_Encodings_1 = []
Face_Names_1 = []
Compare = []

st.session_state["USER-TABLE"] = st.session_state['DATABASE'].select_records(st.session_state['Profile']['config']['table'])
st.session_state["TABLE-FACE-NAME"] = []
for User in st.session_state["USER-TABLE"]:
    st.session_state["TABLE-FACE-NAME"].append(User[2])
st.session_state["TABLE-FACE-ENCODING"] = []
for User in st.session_state["USER-TABLE"]:
    known_face_image = st.session_state['Face_Recognition'].load_image_file(User[3])
    known_face_encoding = st.session_state['Face_Recognition'].face_encodings(known_face_image)[0]
    st.session_state["TABLE-FACE-ENCODING"].append(known_face_encoding)

while not st.session_state['STOP']:
    if st.session_state["LIST-CAMERA"][0] is None:
        break
    if st.session_state["LIST-CAMERA"][1] is None:
        break
    return_0 , frame_0 = st.session_state["LIST-CAMERA"][0].read()
    return_1 , frame_1 = st.session_state["LIST-CAMERA"][1].read()
    st.session_state["COPY-LIST-CAMERA"][0] = frame_0.copy()
    st.session_state["COPY-LIST-CAMERA"][1] = frame_1.copy()
    if not return_0 or frame_0 is None or not return_1 or frame_1 is None:
        break
    if PROCESS_THIS_FRAME:
        Small_Frame_0 = st.session_state['Opencv_Python'].resize(frame_0, (0, 0), fx=0.25, fy=0.25)
        Small_Frame_1 = st.session_state['Opencv_Python'].resize(frame_1, (0, 0), fx=0.25, fy=0.25)
        RGB_Small_Frame_0 = st.session_state['Opencv_Python'].cvtColor(Small_Frame_0, st.session_state['Opencv_Python'].COLOR_BGR2RGB)
        RGB_Small_Frame_1 = st.session_state['Opencv_Python'].cvtColor(Small_Frame_1, st.session_state['Opencv_Python'].COLOR_BGR2RGB)
        Face_Locations_0 = st.session_state['Face_Recognition'].face_locations(RGB_Small_Frame_0)
        Face_Locations_1 = st.session_state['Face_Recognition'].face_locations(RGB_Small_Frame_1)
        Face_Encodings_0 = st.session_state['Face_Recognition'].face_encodings(RGB_Small_Frame_0, Face_Locations_0)
        Face_Encodings_1 = st.session_state['Face_Recognition'].face_encodings(RGB_Small_Frame_1, Face_Locations_1)
        Face_Names_0 = []
        Face_Names_1 = []
        for Face_Encoding in Face_Encodings_0:
            # See if the face is a match for the known face(s)
            Compare = st.session_state['Face_Recognition'].compare_faces(st.session_state["TABLE-FACE-ENCODING"], Face_Encoding)
            name = "Unknown"
            Matches = st.session_state['Face_Recognition'].face_distance(st.session_state["TABLE-FACE-ENCODING"], Face_Encoding)
            if len(Matches) > 0:
                Index = Matches.argmin()
                if Matches[Index] < 0.6:
                    Configure.update_date(st.session_state["USER-TABLE"][Index][2], st.session_state['DATABASE'],st.session_state['Profile']['config']['table'])
                    Face_Names_0.append(st.session_state["TABLE-FACE-NAME"][Index])
                else:
                    Face_Names_0.append("Unknown")
            else:
                Face_Names_0.append("Unknown")
        if True not in Compare:
            st.toast("Camera 1 : Unknown Detect")
        for Face_Encoding in Face_Encodings_1:
            # See if the face is a match for the known face(s)
            Compare = st.session_state['Face_Recognition'].compare_faces(st.session_state["TABLE-FACE-ENCODING"], Face_Encoding)
            name = "Unknown"
            Matches = st.session_state['Face_Recognition'].face_distance(st.session_state["TABLE-FACE-ENCODING"], Face_Encoding)
            if len(Matches) > 0:
                Index = Matches.argmin()
                if Matches[Index] < 0.6:
                    Configure.update_date(st.session_state["USER-TABLE"][Index][1], st.session_state['DATABASE'],st.session_state['Profile']['config']['table'])
                    Face_Names_1.append(st.session_state["TABLE-FACE-NAME"][Index])
                else:
                    Face_Names_1.append("Unknown")
            else:
                Face_Names_1.append("Unknown")
        if True not in Compare:
            st.toast("Camera 2 : Unknown Detect")
    PROCESS_THIS_FRAME = not PROCESS_THIS_FRAME
    for (i, j) in zip(Face_Locations_0, Face_Names_0):
        top, right, bottom, left = i
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        st.session_state['Opencv_Python'].rectangle(frame_0, (left, top), (right, bottom), (0, 0, 255), 2)
        st.session_state['Opencv_Python'].putText(frame_0, j, (left + 6, bottom - 6), st.session_state['Opencv_Python'].FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    for (i, j) in zip(Face_Locations_1, Face_Names_1):
        top, right, bottom, left = i
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        st.session_state['Opencv_Python'].rectangle(frame_1, (left, top), (right, bottom), (0, 0, 255), 2)
        st.session_state['Opencv_Python'].putText(frame_1, j, (left + 6, bottom - 6), st.session_state['Opencv_Python'].FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    VIDEO_0.image(frame_0, channels="BGR")
    VIDEO_1.image(frame_1, channels="BGR")
if st.session_state['STOP']:
    st.session_state['Opencv_Python'].destroyAllWindows()
    Context = st.columns(2)
    with Context[0].popover("Camera 1", use_container_width=True, disabled=not st.session_state['STOP']):
        st.write("Camera 1")
        # st.image(st.session_state["COPY-LIST-CAMERA"][0], channels="BGR",width=200)
        # Convert the frame to RGB format
        Cols_1 , Cols_2 = st.columns(2)
        IMG_1 = st.session_state['Opencv_Python'].cvtColor(st.session_state["COPY-LIST-CAMERA"][0], st.session_state['Opencv_Python'].COLOR_BGR2RGB)
        IMG_PIL_1 = Image.fromarray(IMG_1)
        IMG_PIL_1 = IMG_PIL_1.resize((200, 200))
        with Cols_1 :
            CROP_IMG_1 = st_cropper(IMG_PIL_1, realtime_update=True, box_color='#0000FF', aspect_ratio=None)
            _ = CROP_IMG_1.thumbnail((200,200))
        with Cols_2 :
            st.image(CROP_IMG_1)
    with Context[1].popover("Camera 2", use_container_width=True, disabled=not st.session_state['STOP']):
        st.write("Camera 2")
        # st.image(st.session_state["COPY-LIST-CAMERA"][1], channels="BGR",width=200)
        IMG_2 = st.session_state['Opencv_Python'].cvtColor(st.session_state["COPY-LIST-CAMERA"][1], st.session_state['Opencv_Python'].COLOR_BGR2RGB)    
        IMG_PIL_2 = Image.fromarray(IMG_2)
        Cols_1 , Cols_2 = st.columns(2)
        IMG_PIL_2 = IMG_PIL_2.resize((200, 200))
        with Cols_1 :
            CROP_IMG_2 = st_cropper(IMG_PIL_2, realtime_update=True, box_color='#0000FF', aspect_ratio=None)
            _ = CROP_IMG_2.thumbnail((200,200))
        with Cols_2 :
            st.image(CROP_IMG_2)
        