const { SlashCommandBuilder } = require('@discordjs/builders');
const { Modal, TextInputComponent, showModal } = require('discord-modals')

module.exports = {
    data: new SlashCommandBuilder()
    .setName('embed')
    .setDescription('สร้างประกาศ'),
    async execute(client, interaction) {
        const user_id = interaction.user.id;
        if(!client.config.ownerID.includes(user_id)) return interaction.reply({ content: `คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้`, ephemeral: true });

        const embedmodal = new Modal()
        .setCustomId("embed-id")
        .setTitle("กรอกข้อมูลเพื่อสร้าง Embed")
        .addComponents(
            new TextInputComponent()
            .setCustomId("embed-title")
            .setLabel("ชื่อหัวข้อ | TITLE")
            .setStyle("SHORT")
            .setRequired(false),
            new TextInputComponent()
            .setCustomId("embed-description")
            .setLabel("รายละเอียดข้อความ | DESCRIPTION")
            .setStyle("LONG")
            .setRequired(false),
            new TextInputComponent()
            .setCustomId("embed-img")
            .setLabel("ลิ้งรูปภาพ | URL IMAGE")
            .setStyle("SHORT")
            .setRequired(false),
            new TextInputComponent()
            .setCustomId("embed-color")
            .setLabel("สีของ Embed | COLOR")
            .setStyle("SHORT")
        )
        await showModal(embedmodal, {
            client: client,
            interaction: interaction,
        })
    }
          }