const yearSelect = document.getElementById("year");
const monthSelect = document.getElementById("month");
const daySelect = document.getElementById("day");

for (let y = 1910; y <= 2025; y++) {
    yearSelect.innerHTML += `<option value="${y}">${y}年</option>`;
}
for (let m = 1; m <= 12; m++) {
    monthSelect.innerHTML += `<option value="${m}">${m}月</option>`;
}
for (let d = 1; d <= 31; d++) {
    daySelect.innerHTML += `<option value="${d}">${d}日</option>`;
}

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