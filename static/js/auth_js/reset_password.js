const first_step_container=document.getElementById("first-step");
const last_step_container=document.getElementById("last-step");
const email_inp=document.getElementById("email");
const new_password_inp=document.getElementById("new_password");
const confirm_new_password_inp=document.getElementById("confirm_new_password");
const roles_dropdown=document.getElementById("roles");

let user_type="";
let email="";
let new_password="";

function email_validate(email){
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email)
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

    if(!validatePasswordLength(_new_password,5)){
        $.toast({
            text: `Password must be 5 character long!`,
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