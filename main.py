import nextcord
from nextcord.ext import commands
from os import system 
from colorama import Fore
from time import sleep
import requests


token = os.getenv("TOKEN") #ใส่โทนเคนบอทใน ""
guild_id = 1258352412884860959 #ใส่ไอดีเซิฟเวอร์
channelcommand = 1258352413333655657
prefixs = "/" #เปลี่ยนได้ คำนำหน้า


avatar_url = "https://cdn.discordapp.com/attachments/1322455438863634543/1322477052451880971/IMG_5495.png?ex=67e5083b&is=67e3b6bb&hm=bf35a8753db592bb4bf0d31c4858e9415c4c8ba0500964d066c88ff9e282ee60&" #ใส่ลิ้งรูป




class DeleteWebhook(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="ลบเว็ปฮุ๊ค",
            custom_id="persistent_modal:feedback",
            timeout=None,
        )

        self.a = nextcord.ui.TextInput(
            label="ลิ้งค์เว็ปฮุ๊ค",
            max_length=3000,
            custom_id="persistent_modal:a",
        )
        self.add_item(self.a)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send(embed=embedsucceed)
        requests.delete(self.a.value)

class SpamWebhook(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="สแปมเว็ปฮุ๊ค",
            custom_id="persistent_modal:feedback",
            timeout=None,
        )

        self.b = nextcord.ui.TextInput(
            label="ลิ้งค์เว็ปฮุ๊ค",
            max_length=3000,
            custom_id="persistent_modal:b",
        )
        self.add_item(self.b)

        self.c = nextcord.ui.TextInput(
            label="จำนวน",
            max_length=30,
            custom_id="persistent_modal:c",
        )
        self.add_item(self.c)

        self.d = nextcord.ui.TextInput(
            label="ข้อความ",
            max_length=3000,
            custom_id="persistent_modal:d",
        )
        self.add_item(self.d)

    async def callback(self, interaction: nextcord.Interaction):

        await interaction.send(embed=embedsucceed)
        for i in range(int(self.c.value)):
            requests.post(self.b.value, json = {"content": self.d.value, "username": "ICE OFFICIAL", "avatar_url": avatar_url})

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_modals_added = False

    async def on_ready(self):
        if not self.persistent_modals_added:
            self.add_modal(DeleteWebhook())
            self.add_modal(SpamWebhook())
            self.persistent_modals_added = True
            system('cls')
            print(' -----')
            print('\n > Login....')
            sleep(1)
            system('cls')
            print(' -----')
            print(f'{Fore.GREEN}\n > Login Token client Done!{Fore.RESET}')
            sleep(0.5)
            system('cls')
            print(' -----')
            print(f'\n > Login Token client : {bot.user}')
            print('\n -----')
            await bot.change_presence(activity=nextcord.Game(name="Webhook Bot"))

bot = Bot(command_prefix=prefixs)

# # # # # # # # # # # # 
embedhelp = nextcord.Embed(title="** | ICE OFFICIAL**", description=f"```{prefixs}help = ช่วยเหลือ```\n```{prefixs}delwebhook = ลบเว็ปฮุค```\n```{prefixs}setup = สแปมเว็ปฮุค```", colour=nextcord.Color.blue())  
embedhelp.set_footer(text="terd") #เปลี่ยนได้นะครับ



embedsucceed = nextcord.Embed(title="**Succeed**", description=f"``` ใช้งานสำเร็จ 🟢```", colour=nextcord.Color.green())

embedsucceed.set_image(url="https://cdn.discordapp.com/attachments/1322455438863634543/1322477052451880971/IMG_5495.png?ex=67e5083b&is=67e3b6bb&hm=bf35a8753db592bb4bf0d31c4858e9415c4c8ba0500964d066c88ff9e282ee60&") #ใส่ลิ้งรูปได้


embedsucceed.set_footer(text="data shop") #เปลี่ยนได้นะครับ


@bot.slash_command(
    name="delwebhook",
    description="สำหรับลบเว็ปฮุ๊ค !",
    guild_ids=[guild_id],
)
async def deletewebhook (interaction: nextcord.Interaction):
    if (interaction.channel.id == channelcommand):
        await interaction.response.send_modal(DeleteWebhook())

@bot.slash_command(
    name="setup",
    description="สำหรับสแปมเว็ปฮุ๊ค",
    guild_ids=[guild_id],
)
async def spamwebhook (interaction: nextcord.Interaction):
    if (interaction.channel.id == channelcommand):
        await interaction.response.send_modal(SpamWebhook())

@bot.slash_command(
    name="help",
    description="เมนูคำสั่งบอท",
    guild_ids=[guild_id],
)
async def help (interaction: nextcord.Interaction):
    if (interaction.channel.id == channelcommand):
        await interaction.send(embed=embedhelp)

bot.run(token)
