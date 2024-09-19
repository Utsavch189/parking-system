const close_modal_btn=document.getElementById('close-slot-modal');
const create_facilities_btn=document.getElementById('create-facilities-btn');
const create_open_close_btn=document.getElementById('create-open-close-btn');
const create_btn=document.getElementById('create-btn');

const slot_address_section=document.getElementById('slot-address-section');
const select_facility_section=document.getElementById('select-facility-section');
const open_close_time_container=document.getElementById('open-close-time-container');

const facilities=document.getElementById("facilities");
const facility_container=document.getElementById("facility-container");

let address="";
let direction_address="";

let all_facilities=[];
let displayed_facilities=[];
let selected_facilities=[];

const selected_days=[];
const days = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]

document.addEventListener("DOMContentLoaded",()=>{

    open_close_time_container.innerHTML = "";

    days.forEach((v, i) => {
        const elm = `
            <div class="mb-6">
                <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-[4rem]">
                        <input id="${v}" day='${v}' name="days${i}" type="checkbox" value="${v}"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                        <label class="ms-2 text-sm font-medium text-gray-900 ">${v}</label>
                    </div>
                    <div class="w-full max-w-[7rem]">
                        ${i===0 ? '<label class="ms-2 text-sm font-medium text-gray-900 mb-3">Start time:</label>' : '<p class="hidden"></p>'}
                        <div class="relative">
                            <div class="absolute inset-y-0 end-0 top-0 flex items-center pe-3.5 pointer-events-none">
                                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                                    <path fill-rule="evenodd"
                                        d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4a1 1 0 1 0-2 0v4a1 1 0 0 0 .293.707l3 3a1 1 0 0 0 1.414-1.414L13 11.586V8Z"
                                        clip-rule="evenodd" />
                                </svg>
                            </div>
                            <input type="time" day='${v}' id="start-${v}" name="start-${v}${i}"
                                class="bg-gray-50 starts-time border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                min="09:00" max="18:00" value="00:00" required />
                        </div>
                    </div>
                    <div class="w-full max-w-[7rem]">
                        ${i===0 ? '<label class="ms-2 text-sm font-medium text-gray-900 mb-3">End time:</label>' : '<p class="hidden"></p>'}
                        <div class="relative">
                            <div class="absolute inset-y-0 end-0 top-0 flex items-center pe-3.5 pointer-events-none">
                                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                                    <path fill-rule="evenodd"
                                        d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4a1 1 0 1 0-2 0v4a1 1 0 0 0 .293.707l3 3a1 1 0 0 0 1.414-1.414L13 11.586V8Z"
                                        clip-rule="evenodd" />
                                </svg>
                            </div>
                            <input type="time" day='${v}' id="end-${v}" name="end-${v}${i}"
                                class="bg-gray-50 ends-time border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                min="09:00" max="18:00" value="00:00" required />
                        </div>
                    </div>
                </div>
            </div>
        `;
        open_close_time_container.innerHTML += elm;
    });

    days.forEach((v) => {
        const checkbox = document.getElementById(v);
        const startTimeInput = document.getElementById(`start-${v}`);
        const endTimeInput = document.getElementById(`end-${v}`);

        if (checkbox) {
            checkbox.addEventListener("input", () => {
                console.log(`Checkbox ${v} value changed`);
                const _day=selected_days.filter(p=>p.day===v);
                if(_day.length>0){
                    _day[0]['checked']===true ?_day[0]['checked']=false:_day[0]['checked']=true;
                }
                else{
                    if(startTimeInput?.value!=="00:00" && endTimeInput?.value==="00:00"){
                        let obj={
                            "day":v,
                            "open_time":startTimeInput.value,
                            "close_time":null,
                            "checked":true
                        }
                        selected_days.push(obj);
                    }
                    else if(endTimeInput?.value!=="00:00" && startTimeInput?.value==="00:00"){
                        let obj={
                            "day":v,
                            "open_time":null,
                            "close_time":endTimeInput?.value,
                            "checked":true
                        }
                        selected_days.push(obj);
                    }
                    else if(startTimeInput?.value!=="00:00" && endTimeInput?.value!=="00:00"){
                        let obj={
                            "day":v,
                            "open_time":startTimeInput.value,
                            "close_time":endTimeInput.value,
                            "checked":true
                        }
                        selected_days.push(obj);
                    }
                    else{
                        let obj={
                            "day":v,
                            "open_time":null,
                            "close_time":null,
                            "checked":true
                        }
                        selected_days.push(obj);
                    } 
                    
                }
            });
        }

        if (startTimeInput) {
            startTimeInput.addEventListener("input", () => {
                console.log(`Start time for ${v} changed : ${startTimeInput.value}`);
                const all_start_time=document.querySelectorAll(".starts-time");
                all_start_time.forEach(v=>{
                    if(v.value==="00:00"){
                        v.value=startTimeInput.value;
                        const _day=selected_days.filter(p=>p.day===v.getAttribute('day'));
                        if(_day.length>0){
                            _day[0]['open_time']=startTimeInput.value;
                        }
                    }
                })
                const _day=selected_days.filter(p=>p.day===v);
                if(_day.length>0){
                    _day[0]['open_time']=startTimeInput.value;
                }
            });
        }

        if (endTimeInput) {
            endTimeInput.addEventListener("input", () => {
                console.log(`End time for ${v} changed : ${endTimeInput.value}`);
                const all_end_time=document.querySelectorAll(".ends-time");
                all_end_time.forEach(v=>{
                    if(v.value==="00:00"){
                        v.value=endTimeInput.value;
                        const _day=selected_days.filter(p=>p.day===v.getAttribute('day'));
                        if(_day.length>0){
                            _day[0]['close_time']=endTimeInput.value;
                        }
                    }
                })
                const _day=selected_days.filter(p=>p.day===v);
                if(_day.length>0){
                    _day[0]['close_time']=endTimeInput.value;
                }
            });
        }
    });

    fetch("/admins/all-facilities")
        .then(res => res.json())
        .then(data => {
            all_facilities=[];
            displayed_facilities=[];
            facility_container.innerHTML="";
            facilities.innerHTML=`<option selected>Select Facilities</option>`;
            JSON.parse(data.data)?.map(v => {
                let value = v.fields;
                all_facilities.push(value);
                displayed_facilities.push(value);
                facilities.innerHTML += get_options_child(value.uid, value.facility_value)
            })
        })
})

function remove_area(chip_id){
    const chip=document.getElementById(chip_id);
    facility_container.removeChild(chip);
    const item=all_facilities.filter(p=>p.uid===chip_id);
    displayed_facilities.push(item[0]);
    facilities.innerHTML=`<option selected>Select Facilities</option>`;
    displayed_facilities.map(v=>{
        facilities.innerHTML += get_options_child(v.uid, v.facility_value)
    })
    selected_facilities=selected_facilities.filter(p=>p.uid!==chip_id);
}

function get_options_child(id,name){
    const option=`
        <option value='${id}'>${name}</option>
    `
    return option;
}

function get_chip_child(id,name){
    const chip=`
        <div id='${id}' class="relative grid select-none items-center whitespace-nowrap rounded-lg bg-gray-900 py-1.5 px-3 font-sans text-xs font-bold uppercase text-white">
                <span class="">${name} <i onclick="remove_area('${id}')" class="fa-solid ml-5 cursor-pointer fa-xmark"></i></span>
        </div>
    `
    return chip;
}

facilities.addEventListener("change",()=>{
    const facility_id=facilities.value;
    displayed_facilities=displayed_facilities.filter(p=>p.uid!==facility_id);
    const item=all_facilities.filter(p=>p.uid===facility_id);
    facility_container.innerHTML+=get_chip_child(item[0].uid,item[0].facility_value);
    facilities.innerHTML=`<option selected>Select Facilities</option>`;
    displayed_facilities.map(v=>{
        facilities.innerHTML += get_options_child(v.uid, v.facility_value)
    })
    selected_facilities.push(item[0]);
})

function save_addresses(){
    address=document.getElementById("slot-address").value;
    direction_address=document.getElementById("slot-direction-guidance").value;
    if(address==="" || direction_address===""){
        $.toast({
            text: "please fill all the fields!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return;
    }
    slot_address_section.classList.add("hidden");
    create_facilities_btn.classList.add("hidden");
    select_facility_section.classList.remove("hidden");
    create_open_close_btn.classList.remove("hidden");
}

function save_facilities(){
    if(!selected_facilities.length){
        $.toast({
            text: "please select facilities!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return;
    }
    select_facility_section.classList.add("hidden");
    create_open_close_btn.classList.add("hidden");
    open_close_time_container.classList.remove("hidden");
    create_btn.classList.remove("hidden");
}

function create(){
    let _selected_days=selected_days.filter(p=>p.checked===true);

    if(!_selected_days.length){
        $.toast({
            text: "please select days!",
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        });
        return;
    }
    let f=false;
    
    _selected_days.map((v)=>{
        console.log(v)
        if(!v.day || !v.open_time || !v.close_time || !v.checked){
            $.toast({
                text: "day or open time or close time must be provided!",
                showHideTransition: 'slide',
                bgColor: 'red',
                textColor: 'white',
                allowToastClose: true,
                hideAfter: 1000,
                stack: 5,
                textAlign: 'left',
                position: 'top-left'
            });
            f=true;
            return;
        }
    })
    if(f){
        return;
    }

    let btnText=create_btn.textContent;
    create_btn.disabled=true;
    create_btn.textContent='Loading...';

    fetch('/parking-owner/parking-slot',{
        method:"POST",
        body:JSON.stringify({
            address:address,
            direction_guidance:direction_address,
            facilities:selected_facilities,
            timings:selected_days
        })
    })
    .then(res=>res.json())
    .then(data=>{
        setTimeout(() => {
            window.location.reload();
        }, 300)
    })
    .finally(()=>{
        create_btn.disabled=false;
        create_btn.textContent=btnText;
    })
}