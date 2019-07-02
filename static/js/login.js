function save() {
    var user = document.getElementById("user");
    var pass = document.getElementById('pass');
    sessionStorage.setItem('user', user.value);
    sessionStorage.setItem('pass', pass.value);
}