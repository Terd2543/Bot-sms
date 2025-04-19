const { SlashCommandBuilder } = require('@discordjs/builders');
const { Modal, TextInputComponent, showModal } = require('discord-modals')
const fs = require('fs');

module.exports = {
    data: new SlashCommandBuilder()
    .setName("reg")
    .setDescription("สมัครบัญชี"),
    async execute(client, interaction) {
        const regmodal = new Modal()
        .setCustomId("reg-id")
        .setTitle("ลงทะเบียนสมาชิก")
        .addComponents(
            new TextInputComponent()
            .setCustomId("reg-name")
            .setLabel("ใส่ชื่อ เช่น สำลี")
            .setStyle("SHORT")
            .setMinLength(1)
            .setMaxLength(20)
            .setRequired(true),
            new TextInputComponent()
            .setCustomId("reg-surname")
            .setLabel("ใส่นามสกุล เช่น ศรีจันทร์")
            .setStyle("SHORT")
            .setMinLength(1)
            .setMaxLength(20)
            .setRequired(true)
        )
        await showModal(regmodal, {
            client: client,
            interaction: interaction,
        });
    }
}