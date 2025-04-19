const client = require("../index.js");
const { MessageEmbed } = require("discord.js");
const fs = require('fs');

client.on("modalSubmit", async (i) => {
    const stockdata = JSON.parse(fs.readFileSync('./db/stock.json', 'utf8'));
    if(i.customId === "addstock-id-a") {
        const stockid = i.getTextInputValue("stock-id");
        const stockamout = i.getTextInputValue("addstock-amount");
        if(isNaN(stockamout)) return i.reply({ content: `\`${stockamout}\` ไม่ใช่ตัวเลข` });
        if(!stockdata[stockid]) return i.reply({ content: `ไม่พบสินค้าไอดี \`${stockid}\`` });
        const addstocksuccess = new MessageEmbed()
        .setColor("GREEN")
        .setTitle(`SUCCESS`)
        .setDescription(`เพิ่มสต๊อกสินค้าสำเร็จ\nID: \`${stockid}\`\nจำนวน: \`${stockamout}\``)
        .setFooter({ text: "/stock add" })
        .setTimestamp();
        stockdata[stockid].amout = parseInt(stockdata[stockid].amout) + parseInt(stockamout);
        i.reply({ embeds: [addstocksuccess] });
        fs.writeFileSync('./db/stock.json', JSON.stringify(stockdata, null, '\t'));
    } else if(i.customId === "removestock-id") {
        const removestockid = i.getTextInputValue("removestock-id");
        const removestockamout = i.getTextInputValue("removestock-amount");
        if(isNaN(removestockamout)) return i.reply({ content: `\`${removestockamout}\` ไม่ใช่ตัวเลข` });
        if(!stockdata[removestockid]) return i.reply({ content: `ไม่พบสินค้าไอดี \`${removestockid}\`` });
        const removestocksuccess = new MessageEmbed()
        .setColor("GREEN")
        .setTitle(`SUCCESS`)
        .setDescription(`ลบสต๊อกสินค้าสำเร็จ\nID: \`${removestockid}\`\nจำนวน: \`${removestockamout}\``)
        .setFooter({ text: "/stock remove" })
        .setTimestamp();
        stockdata[removestockid].amout = parseInt(stockdata[removestockid].amout) - parseInt(removestockamout);
        if(stockdata[removestockid].amout < 0) stockdata[removestockid].amout = 0;
        i.reply({ embeds: [removestocksuccess] });
        fs.writeFileSync('./db/stock.json', JSON.stringify(stockdata, null, '\t'));
    }
});