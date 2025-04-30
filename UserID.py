import os
import xml.etree.ElementTree as ET

# ฟังก์ชันดึง UserId
def extract_user_id(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        user_id = None
        candidates = []

        for entry in root.findall('.//boolean'):
            name = entry.get('name')

            # ตรวจหาค่าที่มี "_"
            if 'experiencePlaytimeReported_' in name or 'firstPlayReported_' in name:
                extracted_id = name.split('_')[-1]
                if extracted_id.isdigit() and extracted_id != "-1":
                    candidates.append(int(extracted_id))

        if candidates:
            user_id = max(candidates)  # เลือกค่าที่ถูกต้องที่สุด

        return user_id
    except Exception as e:
        print(f"  ❌ Error parsing {file_path}: {e}")
    return None

# ฟังก์ชันดึง Username (ถ้าใช้)
def extract_username(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for entry in root.findall('.//string'):
            if entry.get('name') == 'username':
                return entry.text
    except Exception as e:
        print(f"  ❌ Error parsing {file_path}: {e}")
    return None

# ดึงข้อมูลจากแอป
def get_user_data(base_path):
    user_data = []
    
    packages = [
        "com.one.one",
        "com.two.two",
        "com.three.three",
        "com.four.four",
        "com.five.five",
        "com.six.six",
        "com.seven.seven",
        "com.eight.eight",
        "com.nine.nine",
        "com.ten.ten"
    ]

    print("\n🚀 **เริ่มดึงข้อมูล...**\n")

    for package in packages:
        print(f"📦 กำลังตรวจสอบ: {package}")

        prefs_path = os.path.join(base_path, package, 'shared_prefs', 'prefs.xml')
        apps_flyer_path = os.path.join(base_path, package, 'shared_prefs', 'APPS_FLYER_SHARED_PREFS.xml')

        if not os.path.exists(apps_flyer_path):
            print(f"  ⚠️ ไม่พบไฟล์ APPS_FLYER_SHARED_PREFS.xml ใน {package}")
            continue

        user_id = extract_user_id(apps_flyer_path)

        if user_id:
            print(f"  ✅ พบ UserId: {user_id} ใน {package}\n")
            user_data.append((package, user_id))
        else:
            print(f"  ❌ ไม่พบ UserId ใน {package}\n")

    print("\n✅ **ดึงข้อมูลเสร็จสิ้น!**\n")
    return user_data

# บันทึกข้อมูลลงไฟล์
def save_to_files(user_data, accounts_path, links_path):
    with open(accounts_path, 'w', encoding='utf-8') as accounts_file, open(links_path, 'w', encoding='utf-8') as links_file:
        for package, user_id in user_data:
            accounts_file.write(f"{package},{user_id}\n")
            links_file.write(f"{package},roblox://placeid=2753915549\n")

    print(f"\n💾 **ข้อมูลถูกบันทึกลงไฟล์:**")
    print(f"📂 {accounts_path}")
    print(f"📂 {links_path}")

# พาธเก็บไฟล์
base_path = '/data/data/'
accounts_file = "/storage/emulated/0/Download/Banana Cat Hub/accounts.txt"
links_file = "/storage/emulated/0/Download/Banana Cat Hub/server_links.txt"

# ดึงข้อมูล
user_data = get_user_data(base_path)

# บันทึกไฟล์ถ้ามีข้อมูล
if user_data:
    save_to_files(user_data, accounts_file, links_file)
else:
    print("\n❌ **ไม่พบข้อมูลที่สามารถบันทึกได้**")
    
