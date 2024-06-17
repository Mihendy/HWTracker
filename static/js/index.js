document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('show-login-form').addEventListener('click', function () {
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
    });

    document.getElementById('show-register-form').addEventListener('click', function () {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    });
});