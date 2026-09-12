// Smart Clinic - main.js

// 时钟显示
function updateClock() {
    const now = new Date();
    const el = document.getElementById('navbar-clock');
    if (el) {
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        el.textContent = now.toLocaleString('zh-CN', options);
    }
}
updateClock();
setInterval(updateClock, 1000);
