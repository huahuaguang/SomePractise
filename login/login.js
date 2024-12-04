const username = document.getElementById('username');
const password = document.getElementById('password');
const error_text = document.querySelector('.error_text');
let userVarify = /^[a-zA-Z0-9_-]{4,16}$/;
let passwordVarify = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;
//
window.onload = function () {
    username.focus();
}

username.addEventListener('blur', function (event) {
    error_text.textContent = "用户名只能是4到16位（字母，数字，下划线，减号）";
    if (userVarify.test(username.value)) {
        error_text.textContent = "";
    }else{
        username.focus();
    }
});

password.addEventListener('blur', function (event) {
    error_text.textContent = "密码必须包括大小写字母和数字";
    if (passwordVarify.test(password.value)) {
        error_text.textContent = "";
    }
});


document.addEventListener('submit', function (e) {
    // 阻止表单默认提交行为
    e.preventDefault();
    const correctUsername = "estera1";
    const correctPassword = "Nchu2024";
    // 使用用户名和密码验证,并给用户提示错误原因
    if (password.value === correctPassword && username.value === correctUsername) {
        window.location.href = 'main_page.html';
    }else if(!passwordVarify.test(password.value)){
        error_text.textContent = "密码必须包括大小写字母和数字";
    }else {
        if(password.value !== correctPassword && username.value !== correctUsername){
            error_text.textContent = "用户名和密码错误";
        }else if(username.value !== correctUsername){
            error_text.textContent = "用户名错误";
        }else if(password.value !== correctPassword){
            error_text.textContent = "密码错误";
        }            
    }
});