from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import locale

# yo we loggin' stuff here just in case things get messy
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

# set up locale so we can format them numbers all Indo style
locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# main brain of the bot: does all the tax math based on what kind it is
def hitung_pajak(jenis_pajak, nilai, kategori_tanggungan="", per_tahun=False):
    kategori_tanggungan = kategori_tanggungan.upper()
    pengurang_tanggungan = 0
    
    # subtract some amount based on how many fam members u got
    if kategori_tanggungan in ["TK/1", "K/1", "K/I/1"]:
        pengurang_tanggungan = 4500000
    elif kategori_tanggungan in ["TK/2", "K/2", "K/I/2"]:
        pengurang_tanggungan = 9000000
    elif kategori_tanggungan in ["TK/3", "K/3", "K/I/3"]:
        pengurang_tanggungan = 13500000

    # let’s figure out what tax we dealin with
    if jenis_pajak.lower() == "pph":
        if not per_tahun:
            nilai = nilai * 12  # convert monthly to yearly if needed
        if nilai <= 60000000:
            return 0, "❌ nah fam, no tax here. u earnin' under 60mil/yr"

        nilai_terkena_pajak = max(0, nilai - pengurang_tanggungan)
        if nilai_terkena_pajak <= 50000000:
            return nilai_terkena_pajak * 0.05, "💼 here's ur income tax (after dependents cut): "
        elif nilai_terkena_pajak <= 250000000:
            return nilai_terkena_pajak * 0.15, "💼 here's ur income tax (after dependents cut): "
        elif nilai_terkena_pajak <= 500000000:
            return nilai_terkena_pajak * 0.25, "💼 here's ur income tax (after dependents cut): "
        else:
            return nilai_terkena_pajak * 0.30, "💼 here's ur income tax (after dependents cut): "
    elif jenis_pajak.lower() == "ppn":
        return nilai * 0.11, "💸 vat comin' at ya: "
    elif jenis_pajak.lower() == "pbb":
        return nilai * 0.005, "🏠 property tax (pbb): "
    elif jenis_pajak.lower() == "pkb":
        return nilai * 0.015, "🚗 vehicle tax (pkb): "
    elif jenis_pajak.lower() == "ppnbm":
        return nilai * 0.2, "🏷️ luxury stuff tax (ppnbm): "
    elif jenis_pajak.lower() == "bphtb":
        return nilai * 0.05, "🏡 land/building ownership tax (bphtb): "
    elif jenis_pajak.lower() == "beamasuk":
        return nilai * 0.1, "🛳️ import duty comin' thru: "
    elif jenis_pajak.lower() == "pajakeksporimpor":
        return nilai * 0.1, "📤 export/import tax: "
    elif jenis_pajak.lower() == "pph final":
        return nilai * 0.005, "✅ final income tax (pph final): "
    else:
        return "⚠️ whoa, that tax type ain't in the list!", "❌ invalid tax type, bruh!"

# when someone first hits up the bot
async def start(update, context):
    await update.message.reply_text(
        "👋 yo! i'm your chill tax bot 🤖\n"
        "💰 just type the tax type and amount like: PKB 1.000.000\n\n"
        "⚡ heads up: if it's PPh, drop your dependent category and whether it's yearly or monthly\n"
        "📍 format goes like: `pph amount category period`\n"
        "📌 need help? hit /help for the full tax menu"
    )

# help section — showin’ all the commands you can use
async def help_command(update, context):
    await update.message.reply_text(
        "📖 tax command list, fam: \n\n"
        "💼 PPh - income tax, give annual/monthly earnings + fam status 🏠\n"
        "💸 PPN - value added tax\n"
        "🏠 PBB - land/property tax\n"
        "🚗 PKB - vehicle tax\n"
        "🏷️ PPnBM - luxury goods tax\n"
        "🏡 BPHTB - land/building rights tax\n"
        "🛳️ Bea Masuk - import tax (type: beamasuk value)\n"
        "📤 Export/Import tax - (type: pajakeksporimpor value)\n"
        "📝 format: `taxtype amount`\n"
        "📍 like: `ppn 5.000.000` 💡\n\n"
        "📌 6 PPh categories: TK/0 → TK/1 → TK/2 → TK/3 → K/0 → K/1 → K/2 → K/3 → K/I/0 → K/I/1 → K/I/2 → K/I/3\n"
        "📝 TK = single folks\n💍 K = married dudes\n🧑🏻‍💻👩🏻‍💻K/I = joint couple stats\n"
        "📝 1, 2, 3 = number of dependents"
    )

# this one handles the actual tax math when u type it in
async def hitung(update, context):
    try:
        pesan = update.message.text.split()
        jenis_pajak = pesan[0]
        nilai = float(pesan[1].replace('.', ''))  # kill those thousand dots
        kategori_tanggungan = ""
        per_tahun = False

        # if it's pph and we got some extra args
        if jenis_pajak.lower() == "pph":
            if len(pesan) >= 3:
                kategori_tanggungan = pesan[2]
            if len(pesan) == 4 and pesan[3].lower() == "tahun":
                per_tahun = True
            if len(pesan) == 4 and pesan[3].lower() == "bulan":
                per_tahun = False

        hasil, pesan_pajak = hitung_pajak(jenis_pajak, nilai, kategori_tanggungan, per_tahun)
        hasil_format = locale.format_string("%.2f", hasil, grouping=True)

        await update.message.reply_text(
            f"{pesan_pajak}Rp {hasil_format} 💵"
        )
    except (IndexError, ValueError):
        await update.message.reply_text(
            "❌ whoops! wrong format, homie. use: taxtype value category [period]\n"
            "📍 like this: PPh 5.000.000 K/1 tahun 💡"
        )

# this the big guy that runs the whole bot
def main():
    TOKEN = "Your_Telegram_Bot_Token_Here"
    application = Application.builder().token(TOKEN).build()

    # addin' all the commands here
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hitung))

    import asyncio
    try:
        asyncio.get_running_loop()
        application.run_polling()
    except RuntimeError:
        asyncio.run(application.run_polling())

if __name__ == "__main__":
    main()
