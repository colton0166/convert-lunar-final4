from flask import Flask, render_template, request, jsonify
from zhdate import ZhDate
import datetime
import os

app = Flask(__name__)

zodiacs = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬']
tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
digits = '〇一二三四五六七八九'
lichun_table = {
    1920: (2, 5), 2022: (2, 4), 2023: (2, 4), 2024: (2, 4), 2025: (2, 3)
}

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

def is_close_date(dt1, dt2, allowed_days=1):
    delta = abs((dt1 - dt2).days)
    return delta <= allowed_days

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))

        if not (1910 <= year <= 2025):
            return jsonify({'error': '年份不支援'}), 400

        try:
            dt = datetime.datetime(year, month, day)
        except ValueError:
            return jsonify({'error': '月日不正確'}), 400

        # 第一次：國曆轉農曆
        lunar_date = ZhDate.from_datetime(dt)

        # 第二次：農曆轉回國曆
        back_to_solar = lunar_date.to_datetime()

        # 比對原始輸入與反查的國曆，允許 ±1天差異
        if not is_close_date(dt, back_to_solar, allowed_days=1):
            return jsonify({'error': '找不到對應農曆，請重新輸入'}), 400

        lunar_month = lunar_date.lunar_month
        is_leap = getattr(lunar_date, 'lunar_leap', False)

        if is_leap:
            lunar_month_str = f"閏{number_to_chinese(lunar_month)}月"
        else:
            lunar_month_str = f"{number_to_chinese(lunar_month)}月"

        lunar_str = f"{number_to_chinese(lunar_date.lunar_year)}年{lunar_month_str}{lunar_day_to_chinese(lunar_date.lunar_day)}"
        suici = get_suici(lunar_date.lunar_year)

        lichun_month, lichun_day = lichun_table.get(year, (2, 4))
        if (month, day) < (lichun_month, lichun_day):
            zodiac_year = year - 1
        else:
            zodiac_year = year
        zodiac = zodiacs[(zodiac_year - 1900) % 12]

        return jsonify({'lunar': lunar_str, 'suici': suici, 'zodiac': zodiac})

    except Exception as e:
        print("查詢失敗：", e)
        return jsonify({'error': '查詢失敗'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
