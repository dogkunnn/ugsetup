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
    # แก้ไขไฟล์ moon.txt
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        
        # แทนที่ newjobid ด้วย new_job_id ใหม่
        print(f"ก่อนการเปลี่ยนใน {file_path}: {content}")
        content = content.replace('newjobid', new_job_id)
        print(f"หลังการเปลี่ยนใน {file_path}: {content}")
        
        # เขียนเนื้อหากลับไปที่ไฟล์
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"ได้ทำการแก้ไข JobId ใน {file_path} เรียบร้อยแล้ว")
    else:
        print(f"ไม่พบไฟล์ {file_path}")

def edit_self(script_path, new_job_id):
    # แก้ไขตัวเอง (สคริปต์นี้)
    with open(script_path, 'r') as file:
        content = file.read()
    
    print(f"ก่อนการเปลี่ยนใน {script_path}: {content}")
    content = content.replace('newjobid', new_job_id)
    print(f"หลังการเปลี่ยนใน {script_path}: {content}")

    # เขียนเนื้อหากลับไปที่ไฟล์
    with open(script_path, 'w') as file:
        file.write(content)
    print("ได้ทำการแก้ไข JobId ในสคริปต์นี้เรียบร้อยแล้ว")

def reset_job_id(file_path):
    # รีเซ็ต JobId กลับเป็น newjobid โดยการแทนที่ค่าปัจจุบันเท่านั้น
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()
        
        # หาบรรทัดที่มีค่า targetJobId แล้วแทนที่เฉพาะค่า JobId ด้วย newjobid
        new_content = []
        for line in content:
            if "local targetJobId =" in line:
                print(f"บรรทัดก่อนการรีเซ็ต: {line.strip()}")
                line = 'local targetJobId = "newjobid"  -- JobId ของเซิร์ฟเวอร์ที่ต้องการ hop ไป\n'
                print(f"บรรทัดหลังการรีเซ็ต: {line.strip()}")
            new_content.append(line)

        # เขียนเนื้อหาที่แก้ไขแล้วกลับไปที่ไฟล์
        with open(file_path, 'w') as file:
            file.writelines(new_content)
        print(f"ได้ทำการรีเซ็ต JobId ใน {file_path} เรียบร้อยแล้ว")
    else:
        print(f"ไม่พบไฟล์ {file_path}")

def close_roblox():
    # ปิดแอพ Roblox
    os.system("am force-stop com.roblox.client")  # ใช้ชื่อ package ของ Roblox

def main():
    file_path = '/storage/emulated/0/Delta/AUTOexecute/moon.txt'
    script_path = os.path.realpath(__file__)  # รับเส้นทางของสคริปต์ปัจจุบัน

    while True:
        display_menu()
        choice = input("เลือกตัวเลือก (1/2/3/4/5/6): ")

        if choice == '1':
            os.system("python3 rejoin.py")  # รัน Python สคริปต์
        elif choice == '2':
            os.system("ls -l")  # แสดงไฟล์ในโฟลเดอร์ปัจจุบัน
        elif choice == '3':
            print("กำลังออกจากโปรแกรม...")
            break
        elif choice == '4':
            new_job_id = input("กรุณากรอก JobId ใหม่: ")
            edit_file(file_path, new_job_id)
            edit_self(script_path, new_job_id)
        elif choice == '5':
            reset_job_id(file_path)
            reset_job_id(script_path)  # รีเซ็ตในสคริปต์นี้ด้วย
        elif choice == '6':
            close_roblox()  # ปิดแอพ Roblox
        else:
            print("ตัวเลือกไม่ถูกต้อง โปรดลองอีกครั้ง.")  # เพิ่มการจัดการในกรณีตัวเลือกผิด

if __name__ == "__main__":
    main()
