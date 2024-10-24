import os

def replace_menu_code(new_code):
    # เส้นทางไปยังไฟล์ menu.py
    menu_path = '/storage/emulated/0/Download/menu.py'  # เปลี่ยนเส้นทางนี้ให้ถูกต้อง

    # ลบโค้ดเดิมและแทนที่ด้วยโค้ดใหม่
    with open(menu_path, 'w') as file:
        file.write(new_code)
    print(f"ได้ทำการแทนที่โค้ดใน {menu_path} เรียบร้อยแล้ว")

def run_menu_script():
    menu_path = '/storage/emulated/0/Download/menu.py'  # เปลี่ยนเส้นทางนี้ให้ถูกต้อง

    # รันไฟล์ menu.py
    if os.path.isfile(menu_path):
        print(f"กำลังรัน {menu_path} ...")
        os.system(f'python3 {menu_path}')
    else:
        print(f"ไม่พบไฟล์ {menu_path}")

# โค้ดใหม่ที่จะนำไปใส่แทนที่ใน menu.py
new_code = '''
import os

def display_menu():
    print("โปรดเลือกตัวเลือกที่ต้องการ:")
    print("1) รัน Python สคริปต์")
    print("2) แสดงไฟล์ในโฟลเดอร์ปัจจุบัน")
    print("3) ออกจากโปรแกรม")
    print("4) แก้ไขไฟล์ moon.txt และสคริปต์นี้")
    print("5) ลบ JobId และเปลี่ยนกลับเป็น newjobid")
    print("6) ปิดแอพ Roblox")

def edit_file(file_path, new_job_id):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        
        print(f"ก่อนการเปลี่ยนใน {file_path}: {content}")
        content = content.replace('newjobid', new_job_id)
        print(f"หลังการเปลี่ยนใน {file_path}: {content}")
        
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"ได้ทำการแก้ไข JobId ใน {file_path} เรียบร้อยแล้ว")
    else:
        print(f"ไม่พบไฟล์ {file_path}")

def edit_self(script_path, new_job_id):
    with open(script_path, 'r') as file:
        content = file.read()
    
    print(f"ก่อนการเปลี่ยนใน {script_path}: {content}")
    content = content.replace('newjobid', new_job_id)
    print(f"หลังการเปลี่ยนใน {script_path}: {content}")

    with open(script_path, 'w') as file:
        file.write(content)
    print("ได้ทำการแก้ไข JobId ในสคริปต์นี้เรียบร้อยแล้ว")

def reset_job_id(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()
        
        new_content = []
        for line in content:
            if "local targetJobId =" in line:
                print(f"บรรทัดก่อนการรีเซ็ต: {line.strip()}")
                line = 'local targetJobId = "newjobid"  -- JobId ของเซิร์ฟเวอร์ที่ต้องการ hop ไป\\n'
                print(f"บรรทัดหลังการรีเซ็ต: {line.strip()}")
            new_content.append(line)

        with open(file_path, 'w') as file:
            file.writelines(new_content)
        print(f"ได้ทำการรีเซ็ต JobId ใน {file_path} เรียบร้อยแล้ว")
    else:
        print(f"ไม่พบไฟล์ {file_path}")

def close_roblox():
    app_packages = [f"com.roblox.clien{char}" for char in "abcdefghijklmnopqrstuvwxyz0123456789"]
    for package in app_packages:
        os.system(f"am force-stop {package}")
    for package in app_packages:
        result = os.popen(f"adb shell pidof {package}").read().strip()
        if result:
            print(f"{package} ยังทำงานอยู่")
        else:
            print(f"{package} ถูกปิดแล้ว")

def main():
    file_path = '/storage/emulated/0/Delta/AUTOexecute/moon.txt'
    script_path = os.path.realpath(__file__)

    while True:
        display_menu()
        choice = input("เลือกตัวเลือก (1/2/3/4/5/6): ")

        if choice == '1':
            os.system('su -c "cd /sdcard/download && export PATH=$PATH:/data/data/com.termux/files/usr/bin && export TERM=xterm-256color && python3 ./rejoin.py"')
        elif choice == '2':
            os.system("ls -l")
        elif choice == '3':
            print("กำลังออกจากโปรแกรม...")
            break
        elif choice == '4':
            new_job_id = input("กรุณากรอก JobId ใหม่: ")
            edit_file(file_path, new_job_id)
            edit_self(script_path, new_job_id)
        elif choice == '5':
            reset_job_id(file_path)
            reset_job_id(script_path)
        elif choice == '6':
            close_roblox()
        else:
            print("ตัวเลือกไม่ถูกต้อง โปรดลองอีกครั้ง.")

if __name__ == "__main__":
    main()
'''

def main():
    while True:
        print("โปรดเลือกตัวเลือก:")
        print("1) ลบและแทนที่โค้ดในไฟล์ menu.py")
        print("2) รันโค้ดในไฟล์ menu.py")
        print("3) ออกจากโปรแกรม")
        choice = input("เลือกตัวเลือก (1/2/3): ")

        if choice == '1':
            replace_menu_code(new_code)  # แทนที่โค้ดใน menu.py
        elif choice == '2':
            run_menu_script()  # รันไฟล์ menu.py
        elif choice == '3':
            print("กำลังออกจากโปรแกรม...")
            break
        else:
            print("ตัวเลือกไม่ถูกต้อง โปรดลองอีกครั้ง.")

if __name__ == "__main__":
    main()
