import json
import os
from datetime import datetime
import streamlit as st
from Base import Configure
if "Loggin_In" not in st.session_state:
    from Tool import Page
    Page.add_page("Final-PFE", "streamlit_app")
    st.switch_page("streamlit_app.py")
# Set Streamlit page configuration with title, layout, and initial sidebar state
st.set_page_config(page_title="DashBoard", layout="centered", initial_sidebar_state="collapsed")

# Initialize session state for page control with predefined pages
st.session_state['Controlle_Pages'].add_page("Final-PFE", "User")
st.session_state['Controlle_Pages'].add_page("Final-PFE", "Camera")
st.session_state['Controlle_Pages'].add_page("Final-PFE", "Setting")

# Apply custom CSS styles to hide Streamlit's default sidebar and toolbar for a cleaner UI
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

# Create a dashboard with two tabs for searching users by image or name
tab1, tab2 = st.tabs(["🖼️ 🔍 Search Image", "📄 🔍 Search Name"])
with tab1:
    # Tab for uploading and searching by image
    Container = st.container(border=True)
    Img = Container.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    Container.button('Search', key='Search-User-Image')
    Context = st.container(border=True)
    if Img:
        # Display uploaded image and perform face recognition
        Context.columns(3)[1].image(Img)
        Unknown = st.session_state['Face_Recognition'].load_image_file(Img)
        NUMBER_FACES = st.session_state['Face_Recognition'].face_locations(Unknown)
        if 0 < len(NUMBER_FACES) < 2:
            Unknown_encoding = st.session_state['Face_Recognition'].face_encodings(Unknown)[0]
            User, Len = Configure.Search_USER(st.session_state['Profile']['config']['table'], Unknown_encoding,
                                              st.session_state['Profile']['config']['table'])
            if User is None:
                # Form for adding a new user if not recognized
                with st.form("FORM-USER-0"):
                    st.markdown('<center> Add new user </center>', unsafe_allow_html=True)
                    st.columns([0.2, 0.6, 0.2])[1].text_input("new Name User : ", value="", key="NEW-NAME-USER-0")
                    st.columns(3)[1].radio("Enter Role User", ["Admin", "User"], horizontal=True,
                                           key="NEW-ROLE-USER-01", index=1)
                    ADD = st.form_submit_button("ADD", use_container_width=True)
                    if ADD:
                        current_time = datetime.now().strftime('%H:%M')
                        current_date = datetime.now().strftime('%Y/%m/%d')
                        Data_ADD = current_date + ' ' + current_time
                        st.session_state['DATABASE'].insert_record(st.session_state['Profile']['config']['table'],
                                                                   {'IdUser': f'User{Len}',
                                                                    'Name': st.session_state['NEW-NAME-USER-0'],
                                                                    'PathImage': f"Base/Data/{st.session_state['Profile']['config']['table']}/Faces/User{Len}.{Img.name.split('.')[1]}",
                                                                    'Date': Data_ADD,
                                                                    'Role': st.session_state['NEW-ROLE-USER-01']})
                        Configure.ADD_Face(st.session_state['Profile']['config']['table'], Unknown_encoding.tolist())
                        with open(os.path.join(f"Base/Data/{st.session_state['Profile']['config']['table']}/Faces",
                                               f"User{Len}.{Img.name.split('.')[1]}"),
                                  "wb") as f:
                            f.write(Img.getbuffer())
                        st.rerun()
            else:
                # Form for updating user information if recognized
                User = Len['ID_User']
                Users = st.session_state['DATABASE'].select_records(st.session_state['Profile']['config']['table'],
                                                                    f'IdUser = \'{User}\'')
                IdUser = Users[0][1]
                IdImage = Users[0][3]
                with st.form("FORM-USER-0"):
                    Name = st.columns([0.2, 0.6, 0.2])[1].text_input("Name User : ", value=Users[0][2], key="NEW-NAME-USER-1")
                    if Users[0][5] == "Admin":
                        Role = st.columns(3)[1].radio("Enter Role User", ["Admin", "User"], horizontal=True,
                                               key="NEW-ROLE-USER-0", index=0)
                    else:
                        Role = st.columns(3)[1].radio("Enter Role User", ["Admin", "User"], horizontal=True,
                                               key="NEW-ROLE-USER-1", index=1)
                    Donne = {}
                    if ';' in Users[0][4]:
                        Date = Users[0][4].split(';')
                        for D in Date :
                            Key = D.split(' ')
                            if Key[0] in Donne :
                                Donne[Key[0]] = Donne[Key[0]] + " || " +Key[1] 
                            else :
                                Donne[Key[0]] = Key[1]
                        st.dataframe(Donne)
                    else:
                        st.columns(3)[1].write(f"Date : {Users[0][4]}")
                    CHANGE = st.form_submit_button("Change", use_container_width=True)
                if CHANGE:
                    # Update the record with IdUser == User2
                    condition = f"IdUser = '{Users[0][1]}'"
                    data = {"Name": Name, "Role": Role}
                    st.session_state['DATABASE'].update_record(table_name=st.session_state['Profile']['config']['table']
                                                               , data=data, condition=condition)
                    st.toast("OK")
                DELETE = st.button("DELETE",key="BUTTON-DELET",use_container_width=True)
                if DELETE:
                    # Step 1: Read the JSON file
                    with open(f"Base/Data/{st.session_state['Profile']['config']['table']}/{st.session_state['Profile']['config']['table']}.json", 'r') as file:
                        data = json.load(file)
                    Id = 0
                    for user in data['faces']:
                        if user['ID_User'] == IdUser :
                            break
                        Id +=1
                    if 'faces' in data and len(data['faces']) > 0:
                        data['faces'].pop(Id) 
                    with open(f"Base/Data/{st.session_state['Profile']['config']['table']}/{st.session_state['Profile']['config']['table']}.json", 'w') as file:
                        json.dump(data, file, indent=4)  # Save the modified data
                    st.session_state['DATABASE'].delete_record(st.session_state['Profile']['config']['table'],f"IdUser = '{IdUser}'")
                    os.remove(IdImage)
                    st.rerun()

        else:
            # Error message for incorrect image input
            st.error("Input Correctly Image With Only One Face")
with tab2:
    
    # Tab for searching users by name
    Container = st.container(border=True)
    NAME = Container.text_input("Name User : ", value='Youssef Salmi')
    SEARCH = Container.button('Search', key='Search-User-Name')
    if SEARCH:
        st.session_state['SEARCH_BY_NAME'] = True
    if st.session_state['SEARCH_BY_NAME'] :
        # Display user information if found
        Context = st.container(border=True)
        Users = st.session_state['DATABASE'].select_records(st.session_state['Profile']['config']['table'],
                                                            f'Name = \'{NAME}\'')
        if Users:
            with st.form("FORM-USER-2"):
                st.columns(3)[1].image(Users[0][3])
                Name = st.columns([0.2, 0.6, 0.2])[1].text_input("Name User : ", value=Users[0][2], key="NEW-NAME-USER-2")
                if Users[0][5] == "Admin":
                    Role = st.columns(3)[1].radio("Enter Role User", ["Admin", "User"], horizontal=True, key="NEW-ROLE-USER-2",
                                           index=0)
                else:
                    Role = st.columns(3)[1].radio("Enter Role User", ["Admin", "User"], horizontal=True, key="NEW-ROLE-USER-3",
                                           index=1)
                Donne = {}
                if ';' in Users[0][4]:
                    Date = Users[0][4].split(';')
                    for D in Date :
                        Key = D.split(' ')
                        if Key[0] in Donne :
                            Donne[Key[0]] = Donne[Key[0]] + " || " +Key[1] 
                        else :
                            Donne[Key[0]] = Key[1]
                    st.dataframe(Donne)
                else:
                    st.columns(3)[1].write(f"Date : {Users[0][4]}")
                CHANGE = st.form_submit_button("Change", use_container_width=True) 
            if CHANGE:
                # Update the record with IdUser == User2
                condition = f"IdUser = '{Users[0][1]}'"
                data = {"Name": Name, "Role": Role}
                st.session_state['DATABASE'].update_record(table_name=st.session_state['Profile']['config']['table']
                                                        , data=data, condition=condition)
                st.session_state['SEARCH_BY_NAME'] = False
                st.rerun()
            DELETE = st.button("DELETE",key="BUTTON-DELET-1",use_container_width=True)
            if DELETE:
                IdUser = Users[0][1]
                IdImage = Users[0][3]
                # Step 1: Read the JSON file
                with open(f"Base/Data/{st.session_state['Profile']['config']['table']}/{st.session_state['Profile']['config']['table']}.json", 'r') as file:
                    data = json.load(file)
                Id = 0
                for user in data['faces']:
                    if user['ID_User'] == IdUser :
                        break
                    Id +=1
                if 'faces' in data and len(data['faces']) > 0:
                    data['faces'].pop(Id) 
                with open(f"Base/Data/{st.session_state['Profile']['config']['table']}/{st.session_state['Profile']['config']['table']}.json", 'w') as file:
                    json.dump(data, file, indent=4)  # Save the modified data
                st.session_state['DATABASE'].delete_record(st.session_state['Profile']['config']['table'],f"IdUser = '{IdUser}'")
                os.remove(IdImage)
                st.rerun()
        else:
            # Error message if user is not found
            st.error("User Not Found")
