const first_step_container=document.getElementById("first-step");
const last_step_container=document.getElementById("last-step");
const email_inp=document.getElementById("email");
const new_password_inp=document.getElementById("new_password");
const confirm_new_password_inp=document.getElementById("confirm_new_password");
const roles_dropdown=document.getElementById("roles");

const password_error=document.getElementById('password_error');
const confirm_password_error=document.getElementById('confirm_password_error');


let user_type="";
let email="";
let new_password="";
let confirm_password="";

const password_max_length=8;
const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

new_password_inp.addEventListener("input",(e)=>{
    if(e.target.value.length<password_max_length){
        new_password_inp.style.borderColor="red";
        password_error.innerText="password must be 8 character long!";
        new_password=e.target.value;
    }
    else if(e.target.value.length>password_max_length){
        new_password_inp.style.borderColor="blue";
        password_error.innerText="";
        e.target.value = e.target.value.slice(0, password_max_length);
        new_password=e.target.value;
        return;
    }
    else{
        new_password_inp.style.borderColor="blue";
        password_error.innerText="";
        new_password=e.target.value;
    }
})

confirm_new_password_inp.addEventListener("input",(e)=>{
    if (e.target.value.length > password_max_length) {
        e.target.value = e.target.value.slice(0, password_max_length);
        confirm_password=e.target.value;
        return;
    }
    if (e.target.value !== new_password) {
        confirm_new_password_inp.style.borderColor = "red";
        confirm_password_error.innerText = "Passwords do not match!";
        confirm_password=e.target.value;
    } else {
        confirm_new_password_inp.style.borderColor="blue";
        confirm_password_error.innerText = "";
        confirm_password=e.target.value;
    }
})

function email_validate(email){
    return email_regex.test(email)
}

function validatePasswordLength(password, length) {
    if (password.length < length || password.length > length) {
        return false
    }
    return true;
}

function otp_send(){
    const _email=email_inp.value;
    email=_email;
    const _new_password=new_password_inp.value;
    new_password=_new_password;
    const _confirm_new_password=confirm_new_password_inp.value;
    const _user_type=roles_dropdown.value;
    user_type=_user_type;

    if (!_email || !_new_password || !_confirm_new_password || !_user_type){
        $.toast({
            text: `All Fields are not provided yet!`,
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return
    }

    if (_confirm_new_password!==_new_password){
        $.toast({
            text: `Passwords are not matched!`,
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return
    }

    if(!validatePasswordLength(_new_password,password_max_length)){
        $.toast({
            text: `Password must be ${password_max_length} character long!`,
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return
    }

    if(!email_validate(_email)){
        $.toast({
            text: `invalid email!`,
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return
    }
    fetch('/auth/reset-password',{
        method:"POST",
        body:JSON.stringify({
            "email":_email,
            "new_password":_new_password,
            "confirm_new_password":_confirm_new_password,
            "user_type":_user_type
        })
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.status===200){
            $.toast({
                text: data.message,
                showHideTransition: 'slide',
                bgColor: 'green',
                textColor: 'white',
                allowToastClose: true,
                hideAfter: 1000,
                stack: 5,
                textAlign: 'left',
                position: 'top-left'
            })
            first_step_container.classList.add("hidden");
            last_step_container.classList.remove("hidden");
        }
        else{
            $.toast({
                text: data.message,
                showHideTransition: 'slide',
                bgColor: 'red',
                textColor: 'white',
                allowToastClose: true,
                hideAfter: 1000,
                stack: 5,
                textAlign: 'left',
                position: 'top-left'
            })
        }
        console.log(data)
    })
}

function verify(){
    const otp_inp=document.getElementById("otp");
    const otp=otp_inp.value;

    if(!otp){
        $.toast({
            text: "Please Put Your OTP",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return;
    }
    if(isNaN(otp)){
        $.toast({
            text: "Invalid OTP",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return;
    }
    if(parseInt(otp)===NaN){
        $.toast({
            text: "Invalid OTP",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return;
    }
    fetch('/auth/reset-password',{
        method:"POST",
        body:JSON.stringify({
            "email":email,
            "new_password":new_password,
            "otp":otp,
            "user_type":user_type
        })
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.status===200){
            $.toast({
                text: data.message,
                showHideTransition: 'slide',
                bgColor: 'green',
                textColor: 'white',
                allowToastClose: true,
                hideAfter: 1000,
                stack: 5,
                textAlign: 'left',
                position: 'top-left'
            })
            setTimeout(()=>{
                window.history.back();
            },500)
        }
        else{
            $.toast({
                text: data.message,
                showHideTransition: 'slide',
                bgColor: 'red',
                textColor: 'white',
                allowToastClose: true,
                hideAfter: 1000,
                stack: 5,
                textAlign: 'left',
                position: 'top-left'
            })
        }
    })
}