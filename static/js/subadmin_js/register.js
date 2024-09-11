const name_inp=document.getElementById('name');
const email_inp=document.getElementById('email');
const phone_inp=document.getElementById('phone');
const password_inp=document.getElementById('password');
const confirm_password_inp=document.getElementById('confirm-password');
const parking_area_choose=document.getElementById('parking-area-choose');
const selected_area_container=document.getElementById('selected-area-container');

const password_error=document.getElementById('password-error');
const confirm_password_error=document.getElementById('confirm-password-error');

const password_max_length=8;
const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

let password="";
let confirm_password="";
let all_parking_areas=[];
let all_parking_areas_for_choose=[];
let selected_areas=[];
let choosed_parking_areas="";

document.addEventListener("DOMContentLoaded",()=>{
    for(let i=0;i<parking_area_choose.getElementsByTagName('option').length;i++){
        const area_name=parking_area_choose.getElementsByTagName('option').item(i).innerText;
        const area_id=parking_area_choose.getElementsByTagName('option').item(i).value;
        if(area_id!=='no'){
            const obj={
                area_name:area_name,
                area_id:area_id
            }
            all_parking_areas.push(obj);
            all_parking_areas_for_choose.push(obj);
        }
    }
})

function remove_area(area_id,container_id,element_id){
    const container=document.getElementById(container_id);
    const element=document.getElementById(element_id);
    container.removeChild(element);
    selected_areas=all_parking_areas.filter(p=>p.area_id!==area_id);
    all_parking_areas_for_choose.push(
        all_parking_areas.filter(p=>p.area_id===area_id)[0]
    );
    parking_area_choose.innerHTML='<option value="no" selected>Choose Parking Area</option>';
    all_parking_areas_for_choose.map((v)=>{
        parking_area_choose.innerHTML+=`<option value='${v.area_id}'>${v.area_name}</option>`;
    })
}

function render_selected_area(area_name,area_id,container){
    const element_id=area_id;
    const chip=`
        <div id='${element_id}' class="relative grid select-none items-center whitespace-nowrap rounded-lg bg-gray-900 py-1.5 px-3 font-sans text-xs font-bold uppercase text-white">
                <span class="">${area_name} <i onclick="remove_area('${area_id}','${container.id}','${element_id}')" class="fa-solid ml-5 cursor-pointer fa-xmark"></i></span>
        </div>
    `
    container.innerHTML+=chip;
}

parking_area_choose.addEventListener("change",(e)=>{
    const value=e.target.value;
    if(value!=='no'){
        const data=all_parking_areas.filter(p=>p.area_id===e.target.value)[0];
        selected_areas.push(data);
        render_selected_area(data.area_name,data.area_id,selected_area_container);
        all_parking_areas_for_choose=all_parking_areas.filter(p=>p.area_id!==e.target.value);
        parking_area_choose.innerHTML='<option value="no" selected>Choose Parking Area</option>';
        all_parking_areas_for_choose.map((v)=>{
            parking_area_choose.innerHTML+=`<option value='${v.area_id}'>${v.area_name}</option>`;
        })
    }
})

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
    if(!selected_areas.length){
        $.toast({
            text: "Please choose parking areas!",
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
    
    selected_areas.map((v)=>{
        if(!choosed_parking_areas.length){
            choosed_parking_areas+=`${v.area_id}`
        }
        else{
            choosed_parking_areas+=`,${v.area_id}`
        }
    })
    parking_area_choose.getElementsByTagName('option').item(0).value=[...new Set(choosed_parking_areas.split(','))].join(',');

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
