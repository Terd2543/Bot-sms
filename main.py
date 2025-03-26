import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ui
import aiohttp
import asyncio
from datetime import datetime, timedelta
import os
# สร้าง instance ของ bot
bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

token = "TOKEN"  # เปลี่ยนเป็น Token ของคุณ

log = 1258352413333655657

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# ตัวแปรสำหรับการจำกัดการใช้งาน
KEY_USAGE_LIMIT = 100
key_usage_count = 0
key_reset_time = None

def check_key_usage():
    global key_usage_count, key_reset_time
    if key_reset_time is None or datetime.now() >= key_reset_time:
        key_usage_count = 0  # รีเซ็ตการนับการใช้งาน
        key_reset_time = datetime.now() + timedelta(hours=1)  # ตั้งเวลารีเซ็ตใหม่
    return key_usage_count, key_reset_time


class BypassSelect(ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Fluxus", emoji="<:fluxus:1251881382188290119>"),
            nextcord.SelectOption(label="Linkvertise", emoji="<:Linkvertise:1266787483169849365>"),
            nextcord.SelectOption(label="Rekonise", emoji="<:Rekonise:1273990792062697595>"),
            nextcord.SelectOption(label="Delta", emoji="<:delta:1251881089300041808>"),
            nextcord.SelectOption(label="Arceus X", emoji="<:spdmarceus:1266761859936292939>"),
            nextcord.SelectOption(label="Work.ink", emoji="🔗"),
            nextcord.SelectOption(label="Mediafire", emoji="<:mediafire1:1289437115230322729>"),
            nextcord.SelectOption(label="Codex", emoji="<:codex:1251880981321879582>"),
            nextcord.SelectOption(label="Trigon", emoji="<:Trigon:1300786550526709821>"),
            nextcord.SelectOption(label="Cryptic", emoji="<:Cryptic:1304387871016222740>"),
        ]
        super().__init__(placeholder="[ 🔑 เลือกบริการบายพาส  ]", options=options, custom_id="bypass_select")

    async def callback(self, interaction: Interaction):
        selected_service = self.values[0]
        await interaction.response.send_modal(BypassModal(selected_service))


class BypassModal(ui.Modal):
    def __init__(self, service_name: str):
        super().__init__(title=f"กรอกลิ้งค์สำหรับ {service_name}")
        self.service_name = service_name
        self.url_input = ui.TextInput(label="ลิ้งค์ที่ต้องการบายพาส", placeholder="ใส่ลิ้งค์ที่ต้องการกั้บบ", required=True)
        self.add_item(self.url_input)

    async def callback(self, interaction: Interaction):
        global key_usage_count

        
        key_usage_count, key_reset_time = check_key_usage()

        if key_usage_count >= KEY_USAGE_LIMIT:
            remaining_time = (key_reset_time - datetime.now()).seconds // 60  # นาทีที่เหลือ
            await interaction.response.send_message(f"> **หมดเวลาแล้ว คุณต้องรออีก {remaining_time} นาที**", ephemeral=True)
            return

        url = self.url_input.value
        
        
        embed_processing = nextcord.Embed(
            title="> **Bypass Slow**",
            description=f">>> กำลังบายพาส: || {url} || \n\n# รอ 5 วินาที",
            color=nextcord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed_processing, ephemeral=True)

        # รอ 5 วินาที
        await asyncio.sleep(5)

        # เรียกใช้งาน API
        result = await bypass_url(url, self.service_name)

        if result:
            key = result.get('key', 'ไม่มีข้อมูล')
            details = result.get('details', 'ไม่มีข้อมูล')

            
            key_usage_count += 1

            embed_success = nextcord.Embed(
                title="> **Bypass key Success**",
                description=f">>> รายละเอียด: || {details} || \n\nรหัสคีย์: **{key}**",
                color=nextcord.Color.green()
            )

            
            new_link_button = ui.Button(label="สนับสนุนโดย", emoji="<:6641ownerorange:1204253287730122782>", style=nextcord.ButtonStyle.link, url="https://discord.gg/k4W9yjg82r")  
            view = ui.View()
            view.add_item(new_link_button)  

            # ส่ง Embed พร้อมปุ่ม
            await interaction.followup.send(embed=embed_success, view=view, ephemeral=True)
            await interaction.user.send(embed=embed_success, view=view)  # ส่ง DM ไปยังผู้ใช้

            
            log_channel = bot.get_channel(log)  
            embed_log = nextcord.Embed(
                title="> **บริการ Bypass key**",
                description=f">>> {interaction.user.name} ได้ใช้บริการ {self.service_name} \nURL: || {url} || \n\nรหัสคีย์: **{key}**",
                color=nextcord.Color.dark_blue()
            )
            await log_channel.send(embed=embed_log)
        else:
            await interaction.followup.send("> ไม่สำเร็จ! กรุณาลองใหม่.", ephemeral=True)

async def bypass_url(url: str, service_name: str):
    api_endpoints = {
        "Fluxus": f"https://api.robloxexecutorth.workers.dev/fluxus?url={url}",
        "Linkvertise": f"https://api.robloxexecutorth.workers.dev/linkvertise?url={url}",
        "Rekonise": f"https://api.robloxexecutorth.workers.dev/rekonise?url={url}",
        "Delta": f"https://api.robloxexecutorth.workers.dev/delta?url={url}",
        "Arceus X": f"https://api.robloxexecutorth.workers.dev/arceusx?url={url}",
        "Work.ink": f"https://api.robloxexecutorth.workers.dev/workink?url={url}",
        "Mediafire": f"https://api.robloxexecutorth.workers.dev/mediafire?url={url}",
        "Codex": f"https://api.robloxexecutorth.workers.dev/codex?url={url}",
        "Trigon": f"https://api.robloxexecutorth.workers.dev/trigon?url={url}",
        "Cryptic": f"https://api.robloxexecutorth.workers.dev/cryptic?url={url}",
    }

    # เรียกใช้ API
    api_url = api_endpoints[service_name]
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


class CheckKeyButton(ui.Button):
    def __init__(self):
        super().__init__(label="เช็คคีย์", emoji="<a:5b_sparkle_hearts:1295022020056318013>", style=nextcord.ButtonStyle.secondary, custom_id="check_key_button")

    async def callback(self, interaction: Interaction):
        global key_usage_count
        key_usage_count, key_reset_time = check_key_usage()

        if key_usage_count < KEY_USAGE_LIMIT:
            remaining_keys = KEY_USAGE_LIMIT - key_usage_count
            
            
            embed_key_check = nextcord.Embed(
                description=f"> คุณยังสามารถใช้คีย์ได้ **{remaining_keys}** ครั้ง",
                color=nextcord.Color.blue()
            )
            await interaction.response.send_message(embed=embed_key_check, ephemeral=True)
        else:
            remaining_time = (key_reset_time - datetime.now()).seconds // 60  # นาทีที่เหลือ
            
            
            embed_timeout = nextcord.Embed(
                title="> หมดเวลา",
                description=f"คุณต้องรออีก **{remaining_time}** นาที",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed_timeout, ephemeral=True)


class LinkButton(ui.Button):
    def __init__(self):
        super().__init__(label=" วิธีบายพาส", emoji="<:_y_:1213820057407459340>", style=nextcord.ButtonStyle.link, url="https://www.youtube.com/@icewen_22")  # เปลี่ยนลิ้งค์ตามที่ต้องการ

@bot.command()
async def by(ctx):
    
    embed = nextcord.Embed(title="> Bypass Menu ICEWEN", description="> **กรุณาเลือกบริการที่คุณต้องการบายพาส**")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1300076562917494826/1300468889771315302/IMG_1171.jpg")
    embed.set_footer(text="icewen_2")
    view = ui.View(timeout=None)
    view.add_item(BypassSelect())
    view.add_item(CheckKeyButton())  
    view.add_item(LinkButton())  
    await ctx.send(embed=embed, view=view)

    
    
    
    


bot.run(token)
