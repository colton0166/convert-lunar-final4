from flask import Flask, render_template, request, jsonify
from zhdate import ZhDate
import datetime
import os

app = Flask(__name__)

zodiacs = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬']
tiangan = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
dizhi = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
digits = '〇一二三四五六七八九'

# 每年立春日期表
lichun_table = {
    1920: (2, 5), 1921: (2, 4), 1922: (2, 4), 1923: (2, 5),
    1924: (2, 5), 1925: (2, 4), 1926: (2, 4), 1927: (2, 4),
    1928: (2, 5), 1929: (2, 4), 1930: (2, 4), 1931: (2, 4),
    1932: (2, 5), 1933: (2, 4), 1934: (2, 4), 1935: (2, 4),
    1936: (2, 5), 1937: (2, 4), 1938: (2, 4), 1939: (2, 4),
    1940: (2, 5), 1941: (2, 4), 1942: (2, 4), 1943: (2, 4),
    1944: (2, 5), 1945: (2, 4), 1946: (2, 4), 1947: (2, 4),
    1948: (2, 5), 1949: (2, 4), 1950: (2, 4), 1951: (2, 4),
    1952: (2, 5), 1953: (2, 4), 1954: (2, 4), 1955: (2, 4),
    1956: (2, 5), 1957: (2, 4), 1958: (2, 4), 1959: (2, 4),
    1960: (2, 5), 1961: (2, 4), 1962: (2, 4), 1963: (2, 4),
    1964: (2, 5), 1965: (2, 4), 1966: (2, 4), 1967: (2, 4),
    1968: (2, 5), 1969: (2, 4), 1970: (2, 4), 1971: (2, 4),
    1972: (2, 5), 1973: (2, 4), 1974: (2, 4), 1975: (2, 4),
    1976: (2, 5), 1977: (2, 4), 1978: (2, 4), 1979: (2, 4),
    1980: (2, 5), 1981: (2, 4), 1982: (2, 4), 1983: (2, 4),
    1984: (2, 5), 1985: (2, 4), 1986: (2, 4), 1987: (2, 4),
    1988: (2, 4), 1989: (2, 4), 1990: (2, 4), 1991: (2, 4),
    1992: (2, 4), 1993: (2, 4), 1994: (2, 4), 1995: (2, 4),
    1996: (2, 4), 1997: (2, 4), 1998: (2, 4), 1999: (2, 4),
    2000: (2, 4), 2001: (2, 4), 2002: (2, 4), 2003: (2, 4),
    2004: (2, 4), 2005: (2, 4), 2006: (2, 4), 2007: (2, 4),
    2008: (2, 4), 2009: (2, 4), 2010: (2, 4), 2011: (2, 4),
    2012: (2, 4), 2013: (2, 4), 2014: (2, 4), 2015: (2, 4),
    2016: (2, 4), 2017: (2, 4), 2018: (2, 4), 2019: (2, 4),
    2020: (2, 4), 2021: (2, 3), 2022: (2, 4), 2023: (2, 4),
    2024: (2, 4), 2025: (2, 3)
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

        # 查農曆
        lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
        lunar_month = lunar_date.lunar_month
        lunar_day = lunar_date.lunar_day

        # 判斷是不是閏月 (注意：zhdate這版要自己查)
        is_leap_month = False
        # 額外查「農曆月是否是閏月」，用補充表查詢，這裡暫時假設沒有(因 zhdate沒有直接提供)
        # → 之後可升級成查天文表格版

        lunar_month_str = f"閏{number_to_chinese(lunar_month)}月" if is_leap_month else f"{number_to_chinese(lunar_month)}月"
        lunar_str = f"{number_to_chinese(lunar_date.lunar_year)}年{lunar_month_str}{lunar_day_to_chinese(lunar_day)}"

        # 立春換生肖
        lichun_month, lichun_day = lichun_table.get(year, (2, 4))
        if (month, day) < (lichun_month, lichun_day):
            zodiac_year = year - 1
        else:
            zodiac_year = year

        zodiac = zodiacs[(zodiac_year - 1900) % 12]
        suici = get_suici(lunar_date.lunar_year)

        return jsonify({'lunar': lunar_str, 'suici': suici, 'zodiac': zodiac})
    
    except Exception as e:
        print("查詢失敗：", e)
        return jsonify({'error': '查詢失敗，請稍後再試'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
