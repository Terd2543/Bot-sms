const Discord = require('discord.js');
const { Client, Collection } = require('discord.js');
const client = new Discord.Client({
    intents: 32767
});
const discordModals = require('discord-modals');
discordModals(client);

module.exports = client;

// โหลด config จากไฟล์ config.json
client.config = require('./config/config.json');

// ดึง token จาก Environment Variable (ถ้ามี)
client.config.token = process.env.DISCORD_TOKEN || client.config.token;

// ตั้งค่าคอนฟิกอื่น ๆ ที่ไม่เป็นความลับ
client.config.ownerID = client.config.ownerID || process.env.OWNER_ID;
client.config.wallet = client.config.wallet || process.env.WALLET;

// ตั้งค่า Slash commands และอื่น ๆ
client.slash = require('./config/slash.json');
client.commands = new Collection();
require("./handler")(client);

// Login โดยใช้ token ที่ดึงจาก Environment Variable หรือจาก config.json
client.login(client.config.token);