import { login } from "../common_js/index.js";

const password_inp = document.getElementById("password");
const email_inp = document.getElementById("email");
const login_btn=document.getElementById("admin_login_btn");

const password_max_length=8;
const password_error=document.getElementById('login_password_error');

password_inp.addEventListener("input",(e)=>{
    if(e.target.value.length<password_max_length){
        password_inp.style.borderColor="red";
        password_error.innerText="password must be 8 character long!";
    }
    else if(e.target.value.length>password_max_length){
        password_inp.style.borderColor="blue";
        password_error.innerText="";
        e.target.value = e.target.value.slice(0, password_max_length);
        return;
    }
    else{
        password_inp.style.borderColor="blue";
        password_error.innerText="";
    }
})

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