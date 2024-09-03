import { login } from "../common_js/index.js";

const password_inp = document.getElementById("password");
const email_inp = document.getElementById("email");
const login_btn=document.getElementById("admin_login_btn");

function logins(e) {
    login(
        e,
        '/admins/login',
        '/admins',
        email_inp,
        password_inp,
        login_btn
    )
}

login_btn.addEventListener("click", logins);