from datetime import datetime
import json
import numpy as np
import face_recognition
# for return confugration of database
def Return_Admin(email, password):
    Admin = None
    with open('Base/Base/Base.json', 'r') as file:
        data = json.load(file)
    for i in data:
        for j in range(len(data[i])):
            if email == data[i][j]['email'] and password == data[i][j]['password']:
                Admin = data[i][j]
    return Admin
# for compare faces add with face in admin json
def Face_Login(Face_Unknown):

    with open('Base/Base/Base.json', 'r') as file:
        data = json.load(file)
    Temp = None
    for i in data:
        for j in range(len(data[i])):
            Temp = np.array(data[i][j]['face'])
            results = face_recognition.compare_faces([Temp], Face_Unknown)
            if results[0]:
                return data[i][j]
    return None
# that function for add new user
def ADD_Face(ID_Admin, Face):
    with open(f'Base/Data/{ID_Admin}/{ID_Admin}.json', 'r') as file:
        data = json.load(file)
    N_User = len(data['faces'])
    New_User = {
        "ID_User": f"User{N_User}",
        "face": Face
    }
    data["faces"].append(New_User)
    with open(f'Base/Data/{ID_Admin}/{ID_Admin}.json', 'r+') as file:
        json.dump(data, file, indent=4)
# SEarch user with face if exist return id of user of not exist return None
def Search_USER(ID_Admin, Face,Table):
    with open(f'Base/Data/{ID_Admin}/{Table}.json', 'r') as file:
        data = json.load(file)
    for i in data:
        for j in data[i]:
            if len(j['face']) != 0:
                Temp = np.array(j['face'])
                results = face_recognition.compare_faces([Temp], Face)
                if results[0]:
                    return j['ID_User'], j
    return None, len(data['faces'])
# that function for update last detect face user
def update_date(id_user, db,table):
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%Y/%m/%d')
    users = db.select_records(f'{table}', f'IdUser = "{id_user}"')
    for user in users:
        if ';' not in user[4]:
            date_old = user[4].split(' ')
            date_new = user[4] + ';' + current_date
            if date_old[1] != current_time:
                time1 = datetime.strptime(date_old[1], "%H:%M")
                time2 = datetime.strptime(current_time, "%H:%M")
                time_diff = time2 - time1
                if time_diff.total_seconds() > 5 * 60:
                    date_new = date_new + ' ' + current_time
                    print(date_new)
                    db.update_record(f'{table}', {'Date': date_new}, f'IdUser = "{id_user}"')
        else:
            date = user[4].split(';')
            date_old = date[len(date) - 1].split(' ')
            date_new = user[4] + ';' + current_date
            if date_old[1] != current_time:
                time1 = datetime.strptime(date_old[1], "%H:%M")
                time2 = datetime.strptime(current_time, "%H:%M")
                time_diff = time2 - time1
                if time_diff.total_seconds() > 5 * 60:
                    date_new = date_new + ' ' + current_time
                    print(date_new)
                    db.update_record(f'{table}', {'Date': date_new}, f'IdUser = "{id_user}"')


def modify_json(admin_name, admin_email, admin_password, camera_0_url, camera_1_url):
    with open('Base/Base/Base.json', 'r') as f:
        data = json.load(f)

    # Find the admin with the given name
    admin = next((a for a in data['admins'] if a['full_name'] == admin_name), None)
    if admin:
        # Update admin's email, password, and camera URLs
        admin['email'] = admin_email
        admin['password'] = admin_password
        admin['config']['camera_index'][0] = camera_0_url
        admin['config']['camera_index'][1] = camera_1_url
    print("OK")
    with open('Base/Base/Base.json', 'w') as f:
        json.dump(data, f, indent=4)