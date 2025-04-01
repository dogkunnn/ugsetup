import os
import json
import xml.etree.ElementTree as ET

# ฟังก์ชันเพื่อดึง User ID จากไฟล์ XML
def extract_user_id(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        user_id = None  # ค่าเริ่มต้นเป็น None

        for entry in root.findall('.//boolean'):
            name = entry.get('name')
            print(f"  🔍 Checking entry: {name}")  # แสดงชื่อที่ถูกพบ

            # ตรวจหาทั้ง 2 กรณี และเลือกอันแรกที่เจอ
            if 'experiencePlaytimeReported_' in name or 'firstPlayReported_' in name:
                extracted_id = name.split('_')[-1]
                if user_id is None:  # ถ้ายังไม่มีค่า user_id ให้ใช้ค่านี้
                    user_id = int(extracted_id)

        return user_id
    except Exception as e:
        print(f"  ❌ Error parsing file {file_path}: {e}")
    return None

# ฟังก์ชันเพื่อดึง Username จากไฟล์ prefs.xml
def extract_username(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for entry in root.findall('.//string'):
            name = entry.get('name')
            if name == 'username':
                username = entry.text
                return username
    except Exception as e:
        print(f"  ❌ Error parsing file {file_path}: {e}")
    return None

# ฟังก์ชันเพื่อดึงข้อมูลจากหลายแพคเกจ
def get_user_data_from_apps(base_path):
    user_data = {}

    packages = [
        "com.one.one",
        "com.two.two",
        "com.three.three",
        "com.four.four",
        "com.five.five"
    ]  # รายชื่อแพคเกจที่ต้องการตรวจสอบ

    print("\n🚀 **เริ่มต้นกระบวนการดึงข้อมูล...**\n")

    for package in packages:
        print(f"📦 กำลังตรวจสอบแพคเกจ: {package}")

        prefs_file_path = os.path.join(base_path, package, 'shared_prefs', 'prefs.xml')
        apps_flyer_file_path = os.path.join(base_path, package, 'shared_prefs', 'APPS_FLYER_SHARED_PREFS.xml')

        # ตรวจสอบว่าแพคเกจมีไฟล์ที่ต้องการหรือไม่
        if not os.path.exists(apps_flyer_file_path) or not os.path.exists(prefs_file_path):
            print(f"  ⚠️ Warning: {package} ไม่พบไฟล์ (prefs.xml หรือ APPS_FLYER_SHARED_PREFS.xml) 🚫\n")
            continue

        # ดึง User ID
        user_id = extract_user_id(apps_flyer_file_path)

        # ดึง Username
        username = extract_username(prefs_file_path)

        # เก็บข้อมูลลง Dictionary
        if user_id and username:
            print(f"  ✅ พบข้อมูล: Username = {username}, UserId = {user_id}\n")
            user_data[package] = {'Username': username, 'UserId': user_id, 'server_link': 'roblox://

placeid=2753915549'}
        else:
            print(f"  ⚠️ ไม่พบข้อมูลที่สมบูรณ์ใน {package}\n")

    print("\n✅ **กระบวนการดึงข้อมูลเสร็จสิ้น!**\n")
    return user_data

# ฟังก์ชันเพื่อบันทึกข้อมูลลงในไฟล์ JSON
def save_to_json(user_data, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    existing_data.update(user_data)  # อัปเดตข้อมูลใหม่

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

# กำหนดเส้นทางของ SharedPreferences
base_path = '/data/data/'

# ดึงข้อมูลจากทุกแพคเกจ
user_data = get_user_data_from_apps(base_path)

# บันทึกข้อมูลถ้ามีข้อมูลที่พบ
if user_data:
    filename = "/storage/emulated/0/Download/user_data.json"
    save_to_json(user_data, filename)
    print(f"\n💾 **ข้อมูลถูกบันทึกลงในไฟล์: {filename}**")
else:
    print("\n❌ **ไม่พบข้อมูลที่สามารถบันทึกได้**")
                
