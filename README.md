### README.md

```markdown
# Telegram Bot - Personal Assistant

A feature-rich Telegram bot designed to provide utility functions like weather forecasting, random number generation, sleep cycle recommendations, and basic calculations.

---

## Features
1. **Weather Forecasting**:
   - Get real-time weather updates for any city using OpenWeatherMap API.
   - Quickly access forecasts for major cities like Hanoi, Ho Chi Minh, and Da Nang.

2. **Random Number Generator**:
   - Generate random numbers within a specified range.

3. **Sleep Cycle Calculator**:
   - Calculate optimal wake-up times based on sleep cycles.

4. **Simple Math Evaluator**:
   - Safely evaluate mathematical expressions.

5. **Interactive Chat**:
   - Echo user messages and provide custom replies.

---

## Commands
- **`/start`**: Greet the user and provide an introduction.
- **`/help`**: Show a list of available commands and usage.
- **`/weather <city>`**: Fetch weather information for the specified city. For example:
  ```
  /weather Hanoi
  ```
  If no city is specified, you can select from suggested cities.
- **`/random <min> <max>`**: Generate a random number within the range `<min>` to `<max>`. Example:
  ```
  /random 1 100
  ```
- **`/sleep`**: Get recommended wake-up times based on sleep cycles.
- **`/tinh <expression>`**: Evaluate a basic mathematical expression. Example:
  ```
  /tinh 5 + 3 * 2
  ```
- **Text Messages**: Reply with an echo of the user's input.

---

## Installation and Setup
### **1. Requirements**
- Python 3.x
- Required Libraries:
  ```bash
  pip install python-telegram-bot --upgrade
  pip install requests
  pip install pytz
  ```

### **2. Setup**
- Clone this repository or copy the script.
- Replace placeholders in the code with your actual tokens:
  - `token`: Telegram Bot Token from [BotFather](https://t.me/BotFather).
  - `OPENWEATHERMAP_API_KEY`: API key from [OpenWeatherMap](https://openweathermap.org/).

### **3. Run the Bot**
- Execute the Python script:
  ```bash
  python3 script.py
  ```

---

## Code Structure
1. **Main Bot Logic**:
   - Handlers for commands (`/start`, `/help`, `/weather`, `/random`, `/sleep`, `/tinh`).
   - Callback handling for city selection buttons in `/weather`.

2. **Utility Functions**:
   - `get_weather`: Fetch weather details from OpenWeatherMap.
   - `safe_eval`: Evaluate mathematical expressions securely.

3. **Interactive Elements**:
   - Inline keyboard buttons for `/weather` to select major cities.

---

## Examples
### **Weather**
Command:
```
/weather Hanoi
```
Response:
```
Thời tiết ở Hanoi:
Mô tả: Trời nắng
Nhiệt độ: 30°C
Cảm giác như: 32°C
Độ ẩm: 70%
Tốc độ gió: 2.5 m/s
```

### **Random Number**
Command:
```
/random 10 50
```
Response:
```
🎲 Số ngẫu nhiên: 27
```

### **Sleep Cycle**
Command:
```
/sleep
```
Response:
```
Bây giờ là 10:30 PM.

Nếu bạn đi ngủ ngay bây giờ, bạn nên cố gắng thức dậy vào một trong những thời điểm sau:

⏰ 12:00 AM cho 1 chu kỳ - ngủ 1.5 tiếng.
⏰ 1:30 AM cho 2 chu kỳ - ngủ 3 tiếng.
⏰ 3:00 AM cho 3 chu kỳ - ngủ 4.5 tiếng.
⏰ 4:30 AM cho 4 chu kỳ - ngủ 6 tiếng.
⏰ 6:00 AM cho 5 chu kỳ - ngủ 7.5 tiếng.

Chúc ngủ ngon! 😴
```

---

## Notes
- The bot is designed for use on [Google Colab](https://colab.research.google.com/) or local Python environments.
- If running on Colab, uncomment the relevant installation lines for `python-telegram-bot`, `nest_asyncio`, and `pytz`.

---

## Future Enhancements
- Add support for more advanced features like task reminders and note-taking.
- Enhance natural language understanding for commands.
