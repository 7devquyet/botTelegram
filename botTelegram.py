# !pip install python-telegram-bot --upgrade
# !pip install nest_asyncio
# !pip install pytz

# import nest_asyncio
import requests
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
from datetime import datetime, timedelta
# import pytz
import re

# Áp dụng nest_asyncio
# nest_asyncio.apply()

# API key từ OpenWeatherMap
OPENWEATHERMAP_API_KEY = '<API_KEY_OPENWEATHERMAP>'

# Hàm bắt đầu bot
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    first_name = user.first_name

    await update.message.reply_text(f'Xin chào <b>{first_name}</b>!\n'
                                    'Gõ /help để xem danh sách các lệnh mà bot hỗ trợ nhé.\n'
                                    'Bạn cũng có thể truy cập nhanh các chức năng bằng cách nhấn nút Menu bên dưới.\n'
                                    'Nếu thấy bot hữu ích, hãy giúp mình chia sẻ với bạn bè nhé! 💚\n'
                                    '👇 (Menu)', parse_mode='HTML')

#Hàm help
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'🔖 Danh sách lệnh:\n'
                                    '\n/random - Tạo số ngẫu nhiên\n'
                                    '/sleep - Tính chu kỳ giấc ngủ\n'
                                    '/weather - Dự báo thời tiết\n'
                                    '/tinh - Tính toán đơn giản')

# Hàm lấy dữ liệu thời tiết từ OpenWeatherMap
def get_weather(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=vi'
    response = requests.get(url)
    data = response.json()

    if data['cod'] != 200:
        return "Không tìm thấy thông tin thời tiết cho thành phố này."

    weather_desc = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    weather_info = (f"Thời tiết ở {city}:\n"
                    f"Mô tả: {weather_desc}\n"
                    f"Nhiệt độ: {temp}°C\n"
                    f"Cảm giác như: {feels_like}°C\n"
                    f"Độ ẩm: {humidity}%\n"
                    f"Tốc độ gió: {wind_speed} m/s")

    return weather_info

# Hàm xử lý lệnh /weather
async def weather(update: Update, context: CallbackContext) -> None:
    if context.args:
        city = ' '.join(context.args)
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
    else:
        keyboard = [[InlineKeyboardButton("Hà Nội", callback_data='Hà Nội'),
                     InlineKeyboardButton("Hồ Chí Minh", callback_data='Ho Chi Minh'),
                     InlineKeyboardButton("Đà Nẵng", callback_data='Đà Nẵng')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            'Sử dụng cú pháp /weather <tên thành phố> hoặc chọn các thành phố lớn ở dưới để xem thời tiết.',
            reply_markup=reply_markup)

# Hàm xử lý callback khi nhấn nút chọn thành phố
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    city = query.data
    weather_info = get_weather(city)
    await query.edit_message_text(text=weather_info)

# Hàm xử lý lệnh /random
async def random_number(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) != 2:
            raise ValueError("Invalid number of arguments")
        min_val = int(args[0])
        max_val = int(args[1])
        random_num = random.randint(min_val, max_val)
        await update.message.reply_text(f'🎲 Số ngẫu nhiên: {random_num}')
    except (ValueError, IndexError):
        await update.message.reply_text('Sử dụng cú pháp /random <số nhỏ nhất> <số lớn nhất> để tạo số ngẫu nhiên.')

# Hàm xử lý lệnh /sleep
async def sleep(update: Update, context: CallbackContext) -> None:
    # Lấy múi giờ cho Hà Nội
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(tz)  # Thời gian hiện tại theo múi giờ Hà Nội
    current_time = now.strftime('%I:%M %p')  # Định dạng thời gian hiện tại
    sleep_cycles = [1.5, 3, 4.5, 6, 7.5, 9]
    wake_up_times = [(now + timedelta(hours=cycle)).strftime('%I:%M %p') for cycle in sleep_cycles]

    response = f"Bây giờ là {current_time}.\n\nNếu bạn đi ngủ ngay bây giờ, bạn nên cố gắng thức dậy vào một trong những thời điểm sau:\n\n"
    for i, time in enumerate(wake_up_times):
        response += f"⏰ {time} cho {i + 1} chu kỳ - ngủ {sleep_cycles[i]} tiếng.\n"

    response += "\nXin lưu ý rằng bạn nên đi ngủ vào những thời điểm này. Con người trung bình mất ~14 phút để đi vào giấc ngủ, vì vậy hãy lên kế hoạch cho phù hợp!\n\nChúc ngủ ngon! 😴"
    await update.message.reply_text(response)

# Hàm an toàn để đánh giá biểu thức toán học
def safe_eval(expr: str) -> float:
    allowed_operators = {'+', '-', '*', '/', '**', '(', ')'}
    # Kiểm tra xem biểu thức chỉ chứa các ký tự cho phép
    if not re.match(r'^[\d+\-*/().\s]+$', expr):
        raise ValueError("Biểu thức chứa ký tự không hợp lệ")

    # Kiểm tra xem chỉ có các toán tử cho phép trong biểu thức
    tokens = re.split(r'(\D+)', expr)
    for token in tokens:
        token = token.strip()
        if token and not token.isdigit() and token not in allowed_operators:
            raise ValueError("Biểu thức chứa toán tử không hợp lệ")

    # Sử dụng eval để đánh giá biểu thức
    return eval(expr)


# Hàm xử lý lệnh /tinh
async def tinh(update: Update, context: CallbackContext) -> None:
    try:
        expression = ' '.join(context.args)
        if not expression:
            raise ValueError("Biểu thức trống")
        result = safe_eval(expression)
        await update.message.reply_text(f'Kết quả: {result}')
    except Exception as e:
        await update.message.reply_text(f'Sử dụng cú pháp /tinh <phép toán>')

# Hàm xử lý tin nhắn
async def reply(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    await update.message.reply_text(f'Bạn vừa nói: {user_message}')

def main() -> None:
    # Nhập mã thông báo của bạn tại đây
    token = '<TOKEN_TELEGRAM_BOT>'

    # Tạo application
    application = Application.builder().token(token).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("random", random_number))
    application.add_handler(CommandHandler("sleep", sleep))
    application.add_handler(CommandHandler("tinh", tinh))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Bắt đầu bot
    application.run_polling()

if __name__ == '__main__':
    main()
