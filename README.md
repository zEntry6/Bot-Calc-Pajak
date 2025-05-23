# 💸 tax it easy bot! 🤖

a chill telegram bot that helps you calculate all your taxes without the headache 💼  
whether it’s income tax, VAT, car tax, or even luxury goods – this bot’s got your back.

## ✨ dope features:

- 🎯 **auto tax calculation** for stuff like:
  - **Income Tax (PPh)** – with dependent categories + monthly/yearly options
  - **VAT (PPN)**
  - **Land & Building Tax (PBB)**
  - **Vehicle Tax (PKB)**
  - **Luxury Goods Tax (PPnBM)**
  - **Property Acquisition Duty (BPHTB)**
  - **Import Duty (Bea Masuk)**
  - **Export/Import Tax**
  - **Final Income Tax (PPh Final)**
- 💬 **simple and clean input format**
- 🛠️ **built with Python + telegram.ext**

## 🧠 how to use the bot:

1. just drop a message in the bot like:
   `ppn 5.000.000`
2. for income tax, add the dependent category and whether it’s per month or year:
   `pph 7.000.000 K/1 month`

> 📌 type `/help` in the bot chat to see all supported tax types

## 🚀 running the bot locally (for devs):

1. clone the repo:
`git clone https://github.com/zEntry6/pajakin-bot.git
cd pajakin-bot`
2. install the dependencies:
   `pip install -r requirements.txt`
3. set your Telegram bot token in the main() function:
   `TOKEN = "Your_Telegram_Bot_Token_Here"`
4. run it:
   `py bot.py`

## 👨‍💻 made by
coded with ☕ + ❤️ by [@zEntry6]([https://github.com/zEntry6)
