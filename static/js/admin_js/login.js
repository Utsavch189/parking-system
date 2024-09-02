import { login } from "../common_js/index.js";

const password_inp = document.getElementById("password");
const email_inp = document.getElementById("email");
let stat=true;


function logins(e) {
    login(
        e,
        '/admins/login',
        '/admins',
        email_inp,
        password_inp
    )
}

document.getElementById("admin_login_btn").addEventListener("click", logins);