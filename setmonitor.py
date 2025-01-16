import os
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import urllib.request

console = Console()

# คีย์ที่ใช้ในการเข้าสู่ระบบ
VALID_KEY = "STRZX160125"  # สามารถเปลี่ยนเป็นคีย์ที่ต้องการ

# ฟังก์ชันสำหรับการตรวจสอบการเข้าสู่ระบบ (Login)
def login():
    console.print("[bold cyan]โปรดกรอกรหัสผ่านเพื่อเข้าสู่ระบบ[/bold cyan]")
    user_key = Prompt.ask("กรอกรหัสผ่าน")

    if user_key == VALID_KEY:
        console.print("[bold green]เข้าสู่ระบบสำเร็จ![/bold green]")
        return True
    else:
        console.print("[bold red]รหัสผ่านไม่ถูกต้อง![/bold red]")
        return False

# ฟังก์ชันสำหรับดาวน์โหลดไฟล์ .py จาก URL
def download_python_file():
    console.print("[bold cyan]ฟังก์ชันติดตั้งไฟล์ .py จาก URL[/bold cyan]")
    files = {
        "1": {"name": "ROKID FREE", "url": "https://raw.githubusercontent.com/thieusitinks/Rokid-Manager/refs/heads/main/Rokid-UgPhone-Free-Tool", "filename": "Rokid-UgPhone-Free-Tool.py"},
        "2": {"name": "ROKID PREMIUM", "url": "https://raw.githubusercontent.com/RokidManager/neyoshiiuem/refs/heads/main/Rokid-UGPhone", "filename": "Rokid-UGPhone.py"},
    }

    # แสดงรายการไฟล์ Python ที่สามารถดาวน์โหลด
    table = Table(title="ติดตั้งไฟล์ Python จาก URL", title_style="bold cyan")
    table.add_column("ตัวเลือก", justify="center", style="bold magenta")
    table.add_column("ชื่อไฟล์", justify="left", style="bold green")
    for key, file in files.items():
        table.add_row(key, file["name"])
    console.print(table)

    # รับค่าจากผู้ใช้
    choice = Prompt.ask("เลือกไฟล์ที่ต้องการดาวน์โหลด [1-2]", choices=files.keys())

    file_name = files[choice]["name"]
    file_url = files[choice]["url"]

    # ตั้งค่าที่เก็บไฟล์ในโฟลเดอร์ดาวน์โหลด
    download_path = os.path.expanduser("~/storage/downloads/" + files[choice]["filename"])

    # ดาวน์โหลดไฟล์ Python
    console.print(f"[bold green]กำลังดาวน์โหลด {file_name}...[/bold green]")
    try:
        urllib.request.urlretrieve(file_url, download_path)
        console.print(f"[bold cyan]ดาวน์โหลด {file_name} สำเร็จ! ไฟล์ถูกเก็บไว้ที่ {download_path}[/bold cyan]")
    except Exception as e:
        console.print(f"[bold red]เกิดข้อผิดพลาดในการดาวน์โหลดไฟล์: {e}[/bold red]")

# ฟังก์ชันอื่นๆ (ไม่เปลี่ยนแปลง)
def run_python_file():
    console.print("[bold cyan]ฟังก์ชันรันไฟล์ Python ที่ดาวน์โหลดมา[/bold cyan]")
    files = {
        "1": {"name": "ROKID FREE", "filename": "Rokid-UgPhone-Free-Tool.py"},
        "2": {"name": "ROKID PREMIUM", "filename": "Rokid-UGPhone.py"},
    }

    table = Table(title="รันไฟล์ Python", title_style="bold cyan")
    table.add_column("ตัวเลือก", justify="center", style="bold magenta")
    table.add_column("ชื่อไฟล์", justify="left", style="bold green")
    for key, file in files.items():
        table.add_row(key, file["name"])
    console.print(table)

    choice = Prompt.ask("เลือกไฟล์ที่ต้องการรัน [1-2]", choices=files.keys())

    file_name = files[choice]["name"]
    file_path = os.path.expanduser("~/storage/downloads/" + files[choice]["filename"])

    console.print(f"[bold green]กำลังรันไฟล์ {file_name}...[/bold green]")
    os.system(f"python3 {file_path}")
    console.print(f"[bold cyan]รันไฟล์ {file_name} สำเร็จ![/bold cyan]")

def install_sub_command():
    console.print("[bold cyan]คำสั่งที่สามารถติดตั้งได้:[/bold cyan]")
    sub_commands = {
        "1": {
            "name": "Rokid Free",
            "command": "pkg update && pkg install python-pip python tsu libexpat openssl -y && pip install requests Flask colorama",
        },
        "2": {
            "name": "Rokid Premium",
            "command": "pkg update && pkg upgrade -y && pkg install python tsu libexpat openssl -y && pip install requests Flask colorama aiohttp",
        },
    }

    table = Table(title="ติดตั้งคำสั่งรีจอยส์", title_style="bold cyan")
    table.add_column("STRZX", justify="center", style="bold magenta")
    table.add_column("V0.1", justify="left", style="bold green")
    for key, sub_cmd in sub_commands.items():
        table.add_row(key, sub_cmd["name"])
    console.print(table)

    choice = Prompt.ask("เลือกคำสั่งที่ต้องการติดตั้ง [1-2]", choices=sub_commands.keys())

    sub_command_name = sub_commands[choice]["name"]
    sub_command = sub_commands[choice]["command"]

    console.print(f"[bold green]กำลังติดตั้ง {sub_command_name}...[/bold green]")
    os.system(sub_command)
    console.print(f"[bold cyan]ติดตั้ง {sub_command_name} สำเร็จ![/bold cyan]")

def main_menu():
    if not login():  # ถ้า Login ไม่สำเร็จจะกลับไปที่หน้า Login
        sys.exit()

    while True:
        os.system('clear')

        table = Table(title="STRZX SETUP", title_style="bold cyan")
        table.add_column("STRZX", justify="center", style="bold magenta")
        table.add_column("V0.1", justify="left", style="bold green")

        table.add_row("1", "ตั้งDPI")
        table.add_row("2", "ติดตั้งไฟล์รีจอยส์")
        table.add_row("3", "ติดตั้งคำสั่งรีจอยส์")
        table.add_row("4", "รันไฟล์รีจอย์")
        table.add_row("5", "ออกจากโปรแกรม")

        console.print(table)

        choice = Prompt.ask("เลือกตัวเลือก [1-5]", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            set_dpi()
        elif choice == "2":
            download_python_file()  # เรียกเมนูดาวน์โหลดไฟล์ Python
        elif choice == "3":
            install_sub_command()  # เรียกเมนูติดตั้งคำสั่ง
        elif choice == "4":
            run_python_file()  # เรียกรันไฟล์ Python ที่ดาวน์โหลด
        elif choice == "5":
            console.print("[bold red]ลาก่อน![/bold red]")
            sys.exit()

        input("\nกด Enter เพื่อกลับไปยังเมนู...")

def set_dpi():
    console.print("[bold cyan]ตั้งค่าขนาด DPI ของหน้าจอ[/bold cyan]")
    new_dpi = Prompt.ask("กรุณากรอกค่า DPI ใหม่ (เนะนำ 600, 650, 700)")
    if new_dpi.isdigit():
        console.print(f"[bold green]กำลังเปลี่ยน DPI เป็น {new_dpi}...[/bold green]")
        os.system(f"wm density {new_dpi}")
        console.print("[bold cyan]เปลี่ยน DPI สำเร็จ! รีสตาร์ทอุปกรณ์เพื่อใช้งานการตั้งค่าใหม่[/bold cyan]")
    else:
        console.print("[bold red]กรุณากรอกตัวเลขที่ถูกต้อง![/bold red]")

if __name__ == "__main__":
    main_menu()
