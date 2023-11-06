document.getElementById('togglePassword').addEventListener('click', function () {
    let passwordField = document.getElementById('field_password1');
    let passwordIcon = this.querySelector('i');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        passwordIcon.classList.remove('fa-eye');
        passwordIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        passwordIcon.classList.remove('fa-eye-slash');
        passwordIcon.classList.add('fa-eye');
    }
});