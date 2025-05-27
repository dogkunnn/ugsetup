import discord
from discord.ext import commands
import os
import asyncio

# ตั้งค่า Token และ Path ของไฟล์
TOKEN = 'YOUR_BOT_TOKEN'  # ใส่ Token ของบอทคุณ
FILE_PATH = '/storage/emulated/0/Delta/AUTOexecute/moon.txt'  # ใส่ตำแหน่งไฟล์ moon.txt

# กำหนด Intents
intents = discord.Intents.default()
intents.messages = True  # ให้บอทสามารถฟังข้อความในช่องแชทได้
intents.message_content = True  # เปิดการใช้งาน Message Content Intent
bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_CHANNEL_ID = None  # ตัวแปรสำหรับเก็บหมายเลขช่องที่ใช้รับค่า targetJobId
panel_message = None  # ตัวแปรสำหรับเก็บข้อความ Panel


class PanelView(discord.ui.View):
    def __init__(self, bot, cog):
        super().__init__(timeout=None)
        self.bot = bot
        self.cog = cog

    @discord.ui.button(label="ลบข้อความทั้งหมด", style=discord.ButtonStyle.danger, custom_id="delete_messages")
    async def delete_messages(self, interaction: discord.Interaction, button: discord.ui.Button):
        global TARGET_CHANNEL_ID, panel_message
        if interaction.channel.id == TARGET_CHANNEL_ID:
            try:
                # ลบข้อความทั้งหมดจากช่อง ยกเว้นข้อความที่เป็น Panel
                async for message in interaction.channel.history(limit=100):
                    if message.id != panel_message.id:  # ข้ามข้อความที่เป็น Panel
                        await message.delete()

                await interaction.response.send_message("✅ ลบข้อความทั้งหมดในช่องเรียบร้อยแล้ว", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("❌ บอทไม่มีสิทธิ์ในการลบข้อความในช่องนี้", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.response.send_message(f"❌ เกิดข้อผิดพลาดในการลบข้อความ: {str(e)}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ คุณไม่ได้อยู่ในช่องที่ตั้งค่าไว้", ephemeral=True)


class DismissView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ปิดข้อความ", style=discord.ButtonStyle.secondary)
    async def dismiss_message(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()  # ลบข้อความเมื่อกดปุ่ม


class MoonBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_job_id = self.load_job_id()  # โหลดค่าเริ่มต้นของ targetJobId

    def load_job_id(self):
        """โหลดค่า targetJobId จากไฟล์"""
        try:
            with open(FILE_PATH, 'r') as file:
                content = file.readlines()
            for line in content:
                if "local targetJobId =" in line:
                    print(f"✅ โหลด targetJobId สำเร็จ: {line.strip()}")
                    return line.strip()
        except FileNotFoundError:
            print(f"❌ ไม่พบไฟล์ {FILE_PATH}")
            return "Not Found"
        return "Not Found"

    def update_job_id(self, new_job_id):
        """อัปเดตค่า targetJobId ในไฟล์"""
        try:
            new_job_id = new_job_id.strip('"')
            with open(FILE_PATH, 'r') as file:
                content = file.readlines()

            for i in range(len(content)):
                if "local targetJobId =" in content[i]:
                    content[i] = f'local targetJobId = "{new_job_id}"\n'
                    break

            with open(FILE_PATH, 'w') as file:
                file.writelines(content)

            self.current_job_id = f'local targetJobId = "{new_job_id}"'
            print(f"✅ อัปเดต targetJobId เป็น: {new_job_id}")

        except FileNotFoundError:
            print(f"❌ ไม่พบไฟล์ {FILE_PATH}")
            self.current_job_id = "Not Found"

    def remove_backticks(self, text):
        """ลบเครื่องหมาย backticks ออกทั้งหมด"""
        if "`" in text:  # เช็คว่ามีเครื่องหมาย backtick ในข้อความ
            cleaned_text = text.replace('`', '')  # ลบทุกตัว `
            return cleaned_text, True  # คืนค่าพร้อมแจ้งว่าได้ลบออก
        else:
            return text, False  # ไม่มีการเปลี่ยนแปลง

    @discord.app_commands.command(name="setup", description="Set the channel for receiving jobId")
    async def setup(self, interaction: discord.Interaction):
        """กำหนดช่องที่บอทจะฟัง"""
        global TARGET_CHANNEL_ID, panel_message

        TARGET_CHANNEL_ID = interaction.channel.id
        with open("channel_id.txt", "w") as f:
            f.write(str(interaction.channel.id))

        # สร้าง Embed Panel
        embed = discord.Embed(
            title="📋 Target Job ID Panel",
            description=f"ช่องนี้ถูกตั้งค่าสำหรับอัปเดตค่า `targetJobId`",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Current Job ID", value=self.current_job_id, inline=False)
        embed.set_footer(text="สามารถใช้ปุ่มด้านล่างจัดการข้อความในช่องนี้")

        # ส่ง Panel พร้อมปุ่ม
        if panel_message:
            await panel_message.delete()
        view = PanelView(bot=self.bot, cog=self)
        panel_message = await interaction.channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"✅ บอทได้ตั้งค่าช่อง {interaction.channel.name} สำหรับรับค่า targetJobId แล้ว", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """ฟังข้อความในช่องที่ตั้งค่า"""
        global TARGET_CHANNEL_ID, panel_message

        if TARGET_CHANNEL_ID and message.channel.id == TARGET_CHANNEL_ID:
            if message.author == bot.user:
                return

            new_job_id = message.content.strip()
            cleaned_job_id, removed_backticks = self.remove_backticks(new_job_id)  # ลบ backticks ถ้ามี

            # ถ้ามีการลบ backticks ออก
            if removed_backticks:
                # ไม่ส่งข้อความบอกว่า "ลบ backticks"
                pass

            if cleaned_job_id:
                self.update_job_id(cleaned_job_id)

                # อัปเดต Panel
                if panel_message:
                    embed = discord.Embed(
                        title="📋 Target Job ID Panel",
                        description=f"ช่องนี้ถูกตั้งค่าสำหรับอัปเดตค่า `targetJobId`",
                        color=discord.Color.blurple(),
                    )
                    embed.add_field(name="Current Job ID", value=self.current_job_id, inline=False)
                    embed.set_footer(text="สามารถใช้ปุ่มด้านล่างจัดการข้อความในช่องนี้")
                    await panel_message.edit(embed=embed)

                # ส่งข้อความแค่ข้อความที่อัปเดต targetJobId
                embed = discord.Embed(
                    description=f"✅ อัปเดต targetJobId เป็น: `{cleaned_job_id}`",
                    color=discord.Color.green(),
                )
                view = DismissView()
                update_message = await message.channel.send(embed=embed, view=view)

                # ลบข้อความที่ผู้ใช้ส่งทันทีหลังจากการอัปเดต
                await message.delete()

                # ลบข้อความที่ส่งไปหลังจาก 10 วินาที
                await asyncio.sleep(10)  # รอ 10 วินาที
                try:
                    await update_message.delete()  # ลบข้อความที่บอทส่งไป
                except discord.HTTPException:
                    pass  # ถ้าเกิดข้อผิดพลาด ให้ข้ามไป

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    await bot.tree.sync()


async def main():
    async with bot:
        await bot.add_cog(MoonBot(bot))
        await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
        
