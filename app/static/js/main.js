/**
 * 聯絡表單前端驗證
 * - 檢查姓名、Email、訊息內容是否填寫
 * - Email 格式驗證
 * - 若有錯誤則顯示提示，阻止表單送出
 */
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        let valid = true;

        // 姓名驗證
        const name = document.getElementById('name');
        const nameError = document.getElementById('nameError');
        if (!name.value.trim()) {
            nameError.classList.remove('hidden');
            valid = false;
        } else {
            nameError.classList.add('hidden');
        }

        // Email 驗證
        const email = document.getElementById('email');
        const emailError = document.getElementById('emailError');
        const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if (!email.value.trim() || !emailPattern.test(email.value.trim())) {
            emailError.classList.remove('hidden');
            valid = false;
        } else {
            emailError.classList.add('hidden');
        }

        // 訊息內容驗證
        const message = document.getElementById('message');
        const messageError = document.getElementById('messageError');
        if (!message.value.trim()) {
            messageError.classList.remove('hidden');
            valid = false;
        } else {
            messageError.classList.add('hidden');
        }

        // 若有欄位未通過驗證，阻止表單送出
        if (!valid) {
            e.preventDefault();
        }
    });
});
