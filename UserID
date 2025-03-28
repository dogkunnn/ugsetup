import os
import json
import xml.etree.ElementTree as ET

# ฟังก์ชันเพื่อดึง User ID จากไฟล์ XML
def extract_user_id(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # ค้นหา <boolean> ที่มีชื่อในรูปแบบ "experiencePlaytimeReported_123456789"
        for entry in root.findall('.//boolean'):
            name = entry.get('name')
            print(f"Checking entry: {name}")  # พิมพ์ชื่อที่ถูกพบใน <boolean>
            if 'experiencePlaytimeReported' in name:
                # แยก User ID จากชื่อใน 'name' โดยใช้การตัดคำจาก '_'
                user_id = name.split('_')[-1]
                return int(user_id)  # แปลง User ID เป็น integer
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
    return None

# ฟังก์ชันเพื่อดึง Username จากไฟล์ prefs.xml
def extract_username(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # ค้นหา <string> ที่มี name="username"
        for entry in root.findall('.//string'):
            name = entry.get('name')
            if name == 'username':
                username = entry.text
                return username
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
    return None

# ฟังก์ชันเพื่อดึงข้อมูลจากหลายแพคเกจ
def get_user_ids_and_usernames_from_multiple_apps(base_path):
    user_data = {}

    # รายชื่อแพคเกจที่เราต้องการค้นหา
    packages = ["com.appme.rov", "com.meepo.rolx", "com.appmrfgtte.rov"]  # ใส่ชื่อแพคเกจที่ต้องการค้นหา

    for package in packages:
        # เส้นทางไฟล์ SharedPreferences ของแต่ละแอป
        prefs_file_path = os.path.join(base_path, package, 'shared_prefs', 'prefs.xml')
        apps_flyer_file_path = os.path.join(base_path, package, 'shared_prefs', 'APPS_FLYER_SHARED_PREFS.xml')

        # ตรวจสอบว่าแพคเกจมีไฟล์ที่ต้องการหรือไม่
        if not os.path.exists(apps_flyer_file_path) or not os.path.exists(prefs_file_path):
            print(f"Warning: {package} does not have the necessary files (prefs.xml or APPS_FLYER_SHARED_PREFS.xml). Skipping this package.")
            continue
        
        # ดึง User ID จากไฟล์ APPS_FLYER_SHARED_PREFS.xml
        user_id = extract_user_id(apps_flyer_file_path)
        
        # ดึง Username จากไฟล์ prefs.xml
        username = extract_username(prefs_file_path)

        # เก็บข้อมูล
        if user_id and username:
            user_data[package] = {'Username': username, 'UserId': user_id, 'server_link': 'ปล่อยว่าง'}
    
    return user_data

# ฟังก์ชันเพื่อบันทึกข้อมูลลงในไฟล์ JSON
def save_to_json(user_data, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # อัพเดทข้อมูล
    existing_data.update(user_data)

    # บันทึกข้อมูล
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

# กำหนดเส้นทางของ SharedPreferences
base_path = '/data/data/'

# ดึงข้อมูลจากทุกแพคเกจที่มีไฟล์ SharedPreferences
user_data = get_user_ids_and_usernames_from_multiple_apps(base_path)

# ถ้ามีข้อมูลใหม่, บันทึกลงไฟล์ JSON
if user_data:
    filename = "/storage/emulated/0/Download/user_data.json"  # ตั้งชื่อไฟล์ JSON ที่จะบันทึก
    save_to_json(user_data, filename)
    print(f"Data saved to {filename}")
else:
    print("No valid data found for the specified packages.")
