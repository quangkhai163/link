import telebot
import asyncio
from telebot import types
from playwright.async_api import async_playwright

# Thay token của bạn tại đây
TOKEN = "7441292874:AAEZBck1OTom82vHwx_0dCweW9mDRqcUUnY"
bot = telebot.TeleBot(TOKEN)

# ====== Hàm vượt link bằng Playwright ======
async def bypass_link(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(5000)

            # Chờ chuyển hướng sang link gốc
            for _ in range(15):
                if page.url != url and "yeumony" not in page.url and "link1s" not in page.url:
                    break
                await page.wait_for_timeout(1000)

            real_url = page.url
            await browser.close()
            return real_url
    except Exception as e:
        return f"❌ Lỗi khi vượt link: {e}"

# ====== Menu /start ======
@bot.message_handler(commands=['start'])
def start(msg):
    name = msg.from_user.first_name or "bạn"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎯 Vượt link rút gọn", "ℹ️ Hướng dẫn")
    markup.row("👤 Liên hệ admin")

    bot.send_message(
        msg.chat.id,
        f"👋 Xin chào {name}!\n\n"
        "Mình là bot giúp bạn vượt các link rút gọn như `link1s.com` và `yeumony.xyz`\n\n"
        "👉 Gửi mình link cần vượt hoặc chọn chức năng bên dưới:",
        reply_markup=markup
    )

# ====== Nút: Hướng dẫn ======
@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Hướng dẫn")
def how_to_use(msg):
    bot.reply_to(msg,
        "📌 Cách sử dụng bot:\n"
        "1. Gửi một link dạng `https://link1s.com/...` hoặc `https://yeumony.xyz/...`\n"
        "2. Bot sẽ tự động vượt và trả về link gốc cho bạn.\n\n"
        "⏳ Quá trình mất vài giây, vui lòng chờ.")

# ====== Nút: Liên hệ admin ======
@bot.message_handler(func=lambda msg: msg.text == "👤 Liên hệ admin")
def contact_admin(msg):
    bot.reply_to(msg, "📬 Liên hệ admin qua Telegram: @qkdzvcl206")  # ← Thay tên bạn ở đây

# ====== Nút: Vượt link rút gọn (gợi nhắc) ======
@bot.message_handler(func=lambda msg: msg.text == "🎯 Vượt link rút gọn")
def bypass_intro(msg):
    bot.reply_to(msg, "📥 Gửi link rút gọn mà bạn muốn vượt nhé!")

# ====== Xử lý khi người dùng gửi link ======
@bot.message_handler(func=lambda msg: msg.text.startswith("http"))
def handle_link(msg):
    url = msg.text.strip()
    bot.reply_to(msg, "⏳ Đang vượt link, vui lòng chờ vài giây...")

    result = asyncio.run(bypass_link(url))
    bot.send_message(msg.chat.id, f"✅ Link gốc:\n{result}")

# ====== Khởi động bot ======
print("🤖 Bot vượt link đang chạy...")
bot.polling()