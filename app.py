from flask import Flask, render_template, request, jsonify
from zhdate import ZhDate
import datetime
import os

app = Flask(__name__)

zodiacs = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬']
tiangan = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
dizhi = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
digits = '〇一二三四五六七八九'

lichun_table = {year: (2, 4) for year in range(1910, 2026)}
lichun_table[2021] = (2, 3)
lichun_table[2025] = (2, 3)

def number_to_chinese(number):
    return ''.join(digits[int(d)] for d in str(number))

def lunar_day_to_chinese(day):
    if day <= 10:
        return f"初{digits[day]}"
    elif day < 20:
        return f"十{digits[day % 10]}"
    elif day == 20:
        return "二十"
    elif day < 30:
        return f"廿{digits[day % 10]}"
    elif day == 30:
        return "三十"

def get_suici(year):
    return tiangan[(year - 4) % 10] + dizhi[(year - 4) % 12]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    year = int(data.get('year'))
    month = int(data.get('month'))
    day = int(data.get('day'))

    if year < 1920 or year > 2025:
        return jsonify({'error': '只支援 1920 年到 2025 年的資料！'}), 400

    try:
        lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))

        # 關鍵：優先判斷是否是閏月（若不支援前程式設計）
        month_str = f"{number_to_chinese(lunar_date.lunar_month)}月"

        lunar_str = f"{number_to_chinese(lunar_date.lunar_year)}年{month_str}{lunar_day_to_chinese(lunar_date.lunar_day)}"
        suici = get_suici(lunar_date.lunar_year)

        lichun_month, lichun_day = lichun_table.get(year, (2, 4))
        if (month, day) < (lichun_month, lichun_day):
            zodiac_year = year - 1
        else:
            zodiac_year = year
        zodiac = zodiacs[(zodiac_year - 1900) % 12]

        return jsonify({'lunar': lunar_str, 'suici': suici, 'zodiac': zodiac})

    except Exception as e:
        return jsonify({'error': '查詢失敗，請稍後再試'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
