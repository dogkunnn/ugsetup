import discord
from discord import app_commands
from discord.ext import commands

# ตั้งค่า Token และ Path ของไฟล์
TOKEN = 'YOUR_BOT_TOKEN'  # ใส่ Token ของบอทคุณ
FILE_PATH = '/storage/emulated/0/Delta/AUTOexecute/moon.txt'  # ใส่ตำแหน่งไฟล์ moon.txt

# กำหนด Intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


class MoonBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="edit", description="Edit the targetJobId in moon.txt")
    @app_commands.describe(job_id="Enter the new targetJobId")
    async def edit(self, interaction: discord.Interaction, job_id: str):
        """คำสั่งแก้ไข targetJobId"""
        try:
            # อ่านค่าเดิมจากไฟล์
            with open(FILE_PATH, 'r') as file:
                content = file.readlines()

            # ค้นหาค่าเดิมของ targetJobId
            old_value = None
            for line in content:
                if "local targetJobId =" in line:
                    old_value = line.strip()
                    break

            if old_value is None:
                await interaction.response.send_message(
                    "❌ **Error:** `targetJobId` not found in the file.",
                    ephemeral=True
                )
                return

            # แก้ไขค่าที่ต้องการ
            for i in range(len(content)):
                if "local targetJobId =" in content[i]:
                    content[i] = f'local targetJobId = "{job_id}"\n'
                    break

            # เขียนค่าใหม่กลับเข้าไฟล์
            with open(FILE_PATH, 'w') as file:
                file.writelines(content)

            # ส่งข้อความตอบกลับ
            embed = discord.Embed(
                title="✅ File Updated Successfully",
                color=discord.Color.green()
            )
            embed.add_field(name="Before", value=f"```lua\n{old_value}\n```", inline=False)
            embed.add_field(name="After", value=f"```lua\nlocal targetJobId = \"{job_id}\"\n```", inline=False)
            embed.set_footer(text="แก้ไขค่า targetJobId สำเร็จ!")

            await interaction.response.send_message(embed=embed)

        except FileNotFoundError:
            await interaction.response.send_message(
                "❌ **Error:** The file `moon.txt` was not found.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ **An error occurred:** {e}",
                ephemeral=True
            )

    @app_commands.command(name="check", description="Check the current targetJobId in moon.txt")
    async def check(self, interaction: discord.Interaction):
        """คำสั่งตรวจสอบ targetJobId"""
        try:
            # อ่านค่าเดิมจากไฟล์
            with open(FILE_PATH, 'r') as file:
                content = file.readlines()

            # ค้นหาค่า targetJobId
            job_id = None
            for line in content:
                if "local targetJobId =" in line:
                    job_id = line.strip()
                    break

            if job_id is None:
                await interaction.response.send_message(
                    "❌ **Error:** `targetJobId` not found in the file.",
                    ephemeral=True
                )
                return

            # ส่งข้อความตอบกลับ
            embed = discord.Embed(
                title="🔍 Current targetJobId",
                description=f"```lua\n{job_id}\n```",
                color=discord.Color.blue()
            )
            embed.set_footer(text="ตรวจสอบค่า targetJobId สำเร็จ!")

            await interaction.response.send_message(embed=embed)

        except FileNotFoundError:
            await interaction.response.send_message(
                "❌ **Error:** The file `moon.txt` was not found.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ **An error occurred:** {e}",
                ephemeral=True
            )


# เพิ่มคำสั่งใน Slash Commands
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    try:
        await bot.tree.sync()  # ซิงค์คำสั่ง Slash
        print("✅ Slash commands synced!")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


async def main():
    async with bot:
        # เพิ่ม Cog ในบอท
        await bot.add_cog(MoonBot(bot))
        await bot.start(TOKEN)

# เริ่มต้นโปรแกรม
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
