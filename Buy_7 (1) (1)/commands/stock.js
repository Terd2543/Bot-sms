const { SlashCommandBuilder } = require('@discordjs/builders');
const { Modal, TextInputComponent, showModal } = require('discord-modals')

module.exports = {
    data: new SlashCommandBuilder()
    .setName("stock")
    .setDescription("จัดการสต๊อกสินค้า")
    .addSubcommand(subcommand =>
        subcommand
        .setName("add")
        .setDescription("เพิ่มสต๊อกสินค้า")
    )
    .addSubcommand(subcommand =>
        subcommand
        .setName("remove")
        .setDescription("ลบสต๊อกสินค้า")
    ),
    async execute(client, interaction) {
        const user_id = interaction.user.id;
        if(!client.config.ownerID.includes(user_id)) return interaction.reply({ content: "คุณไม่มีสิทธิ์ใช้คำสั่งนี้" });
        if(interaction.options.getSubcommand() === "add") {
            const addstockmodal = new Modal()
            .setCustomId('addstock-id-a')
            .setTitle('เพิ่มสต๊อกสินค้า')
            .addComponents(
                new TextInputComponent()
                .setCustomId('stock-id')
                .setLabel('รหัสสินค้า')
                .setStyle("SHORT")
                .setRequired(true),
                new TextInputComponent()
                .setCustomId('addstock-amount')
                .setLabel('จำนวนสินค้าที่ต้องการเพิ่ม')
                .setStyle("SHORT")
                .setRequired(true)
            )
            await showModal(addstockmodal, {
                client: client,
                interaction: interaction,
            })
        } else if (interaction.options.getSubcommand() === "remove") {
            const removestockmodal = new Modal()
            .setCustomId('removestock-id')
            .setTitle('ลบสต๊อกสินค้า')
            .addComponents(
                new TextInputComponent()
                .setCustomId('removestock-id')
                .setLabel('รหัสสินค้า')
                .setStyle("SHORT")
                .setRequired(true),
                new TextInputComponent()
                .setCustomId('removestock-amount')
                .setLabel('จำนวนสินค้าที่ต้องการลบ')
                .setStyle("SHORT")
                .setRequired(true)
            )
            await showModal(removestockmodal, {
                client: client,
                interaction: interaction,
            })
        }
    }
}