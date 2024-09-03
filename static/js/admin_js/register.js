const name_inp=document.getElementById('name');
const email_inp=document.getElementById('email');
const phone_inp=document.getElementById('phone');
const password_inp=document.getElementById('password');
const confirm_password_inp=document.getElementById('confirm-password');
const pincode_inp=document.getElementById('pincode');

const password_error=document.getElementById('password-error');
const confirm_password_error=document.getElementById('confirm-password-error');

const password_max_length=8;
const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

let password="";
let confirm_password="";

password_inp.addEventListener("input",(e)=>{
    if(e.target.value.length<password_max_length){
        password_inp.style.borderColor="red";
        password_error.innerText="password must be 8 character long!";
        password=e.target.value;
    }
    else if(e.target.value.length>password_max_length){
        password_inp.style.borderColor="blue";
        password_error.innerText="";
        e.target.value = e.target.value.slice(0, password_max_length);
        password=e.target.value;
        return;
    }
    else{
        password_inp.style.borderColor="blue";
        password_error.innerText="";
        password=e.target.value;
    }
})

confirm_password_inp.addEventListener("input",(e)=>{
    if (e.target.value.length > password_max_length) {
        e.target.value = e.target.value.slice(0, password_max_length);
        confirm_password=e.target.value;
        return;
    }
    if (e.target.value !== password) {
        console.log('a')
        confirm_password_inp.style.borderColor = "red";
        confirm_password_error.innerText = "Passwords do not match!";
        confirm_password=e.target.value;
    } else {
        confirm_password_inp.style.borderColor="blue";
        confirm_password_error.innerText = "";
        confirm_password=e.target.value;
    }
})

function validateForm() {
    if(password!==confirm_password){
        $.toast({
            text: "Passwords are not matched!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1400,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return false;
    }
    if(password.length!==password_max_length){
        $.toast({
            text: "Password should be 8 character long!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1400,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return false;
    }
    if(!email_regex.test(email_inp.value)){
        $.toast({
            text: "Email is not valid!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1400,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return false;
    }
    if(isNaN(pincode_inp.value)){
        $.toast({
            text: "Pincode should contain only numbers!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1400,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return false;
    }
    if(isNaN(phone_inp.value) || phone_inp.value.length<10 || phone_inp.value.length>10){
        $.toast({
            text: "Phone number invalid!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1400,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return false;
    }
    return true;
}

$(document).ready(function() {
    $('#countrycode').select2({
        placeholder: "Select a country",
        ajax: {
            url: '/admins/search-country',  // URL to your search view
            dataType: 'json',
            delay: 250,  // Delay for debounce
            data: function (params) {
                return {
                    search: params.term  // Pass the search term to the server
                };
            },
            processResults: function (data) {
                return {
                    results: $.map(data.results, function(country) {
                        return {
                            id: country.country,  // Unique ID for each country
                            text: country.country,  // Text to display in the dropdown
                        }
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 1  // Start searching after one character input
    });
});
