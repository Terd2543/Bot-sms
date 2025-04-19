const client = require("../index.js");
const { MessageEmbed } = require("discord.js");
const fs = require('fs');

client.on("modalSubmit", async (i) => {
    const user_id = i.user.id;
    const name = i.getTextInputValue("reg-name");
    const surname = i.getTextInputValue("reg-surname");
    const accdata = JSON.parse(fs.readFileSync('./db/acc.json', 'utf8'));
    if(i.customId === "reg-id") {
        await i.deferReply({ ephemeral: true });
        const chokun = new MessageEmbed()
        .setColor("RED")
        .setTitle("ผิดพลาด : คุณมีบัญชีแล้ว <a:b5:901051139410239559>")  
        if(accdata[user_id]) return i.followUp({ embeds: [chokun] });
        const embed = new MessageEmbed()
        .setColor("GREEN")
        .setAuthor(`${i.guild.name}`, i.guild.iconURL())
        .setTitle(``)
        .setDescription(`> ✅︱สมัครบัญชีสำเร็จ \n> 📷︱กรุณาแคปหน้าจอเพื่อเป็นหลักฐาน \n\n📝︱รายละเอียดบัญชี \n\nชื่อ-นามสกุล : ||${name} ${surname}|| \nหากต้องการเติมเงิน /topup`)
        .setFooter(`${client.user.tag}`,i.user.avatarURL())
        .setThumbnail(i.user.avatarURL())
        .setTimestamp();
        
        i.followUp({ embeds: [embed] });
        
        accdata[user_id] = {
            name: name,
            surname: surname,

            point: 0,
            pointall: 0
        }
        fs.writeFileSync('./db/acc.json', JSON.stringify(accdata, null, '\t'));
    }
});