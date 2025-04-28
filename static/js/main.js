const yearSelect = document.getElementById("year");
const monthSelect = document.getElementById("month");
const daySelect = document.getElementById("day");

function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

function updateDays() {
    const year = parseInt(yearSelect.value);
    const month = parseInt(monthSelect.value);

    let daysInMonth = 31; // 預設31天
    if (month === 2) {
        daysInMonth = isLeapYear(year) ? 29 : 28;
    } else if ([4, 6, 9, 11].includes(month)) {
        daysInMonth = 30;
    }

    daySelect.innerHTML = "";
    for (let d = 1; d <= daysInMonth; d++) {
        daySelect.innerHTML += `<option value="${d}">${d}日</option>`;
    }
}

// 初始生成年月
for (let y = 1910; y <= 2025; y++) {
    yearSelect.innerHTML += `<option value="${y}">${y}年</option>`;
}
for (let m = 1; m <= 12; m++) {
    monthSelect.innerHTML += `<option value="${m}">${m}月</option>`;
}

// 當年、當月初始化日子
updateDays();

// 當年或月變動時，重新更新日子
yearSelect.addEventListener('change', updateDays);
monthSelect.addEventListener('change', updateDays);

async function convert() {
    const res = await fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            year: yearSelect.value,
            month: monthSelect.value,
            day: daySelect.value
        })
    });
    const data = await res.json();
    const resultDiv = document.getElementById("result");

    if (data.error) {
        resultDiv.innerText = "查詢失敗：" + data.error;
    } else {
        resultDiv.innerHTML = `農曆：${data.lunar}<br>歲次：${data.suici}<br>生肖：${data.zodiac}`;
    }
}
