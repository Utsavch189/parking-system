const area_name_section = document.getElementById('area-name-section');
const select_facility_section = document.getElementById('select-facility-section');
const create_facilities_btn = document.getElementById('create-facilities-btn');
const create_open_close_btn = document.getElementById("create-open-close-btn");
const create_btn = document.getElementById('create-btn');
const select_facility = document.getElementById("facilities");
const modal_body = document.getElementById("main-body-create-parking");
const area_name = document.getElementById('area-name');
const facility_container = document.getElementById("facility-container");
const open_close_time_container = document.getElementById("open-close-time-container");

let facilities = [];
let choosed_facilities=[];
let area = "";
let selected_facilities = [];
const days = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]

const selected_days=[];

document.addEventListener("DOMContentLoaded", () => {
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
                    }
                    const _day=selected_days.filter(p=>p.day===v.getAttribute('day'));
                    if(_day.length>0){
                        _day[0]['open_time']=startTimeInput.value;
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
});


function create_open_close_time() {
    let f=false;
    console.log(selected_facilities)
    if (!selected_facilities.length) {
        $.toast({
            text: "please select facilities",
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

    selected_facilities.map((v) => {
        console.log(v)
        if (!v.charges || !v.penalty_charge_per_hour) {
            $.toast({
                text: "charges and penalty charges must not be empty",
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
        if (isNaN(v.charges) || isNaN(v.penalty_charge_per_hour)) {
            $.toast({
                text: "charges and penalty charges must be a valid number",
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
    create_open_close_btn.classList.add("hidden");
    select_facility_section.classList.add("hidden");
    create_btn.classList.remove("hidden");
    open_close_time_container.classList.remove("hidden");
}

function submit_area_name() {
    console.log(area_name.value)
    if (!area_name.value) {
        $.toast({
            text: "area name is required!",
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
    let text=create_facilities_btn.textContent;
    create_facilities_btn.disabled=true;
    create_facilities_btn.textContent='Loading...';
    fetch('/admins/parking-area', {
        method: "POST",
        body: JSON.stringify({ "area_name": area_name.value })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === 200) {
                area_name_section.classList.add("hidden");
                select_facility_section.classList.remove("hidden");
                create_facilities_btn.classList.add("hidden");
                create_open_close_btn.classList.remove("hidden");
                area = area_name.value;
            }
        })
        .finally(()=>{
            create_facilities_btn.disabled=false;
            create_facilities_btn.textContent=text;
        })
}

function get_options_child(value, name) {
    return `
        <option value=${value}>${name}</option>
    `
}


function set_charges(facility_id, input_id, charge_type) {
    // charge_type = 'charge' or 'penalty'
    console.log(facility_id)
    if (charge_type === 'charge') {
        var charge_inp_id = input_id.toString();
        let facility = selected_facilities.filter(p => p.id === facility_id);
        if (!facility.length) {
            const facility_obj = {
                id: facility_id,
                charges: document.getElementById(charge_inp_id).value,
                penalty_charge_per_hour: null
            };
            selected_facilities.push(facility_obj);
        }
        else {
            facility[0]['charges'] = document.getElementById(charge_inp_id).value;
        }
    }
    else if (charge_type === 'penalty') {
        var penalty_charge_inp_id = input_id.toString();
        let facility = selected_facilities.filter(p => p.id === facility_id);
        if (!facility.length) {
            const facility_obj = {
                id: facility_id,
                charges: null,
                penalty_charge_per_hour: document.getElementById(penalty_charge_inp_id).value
            };
            selected_facilities.push(facility_obj);
        }
        else {
            facility[0]['penalty_charge_per_hour'] = document.getElementById(penalty_charge_inp_id).value;
        }
    }

}

function canceled_facility(id, container_id, facility_id) {
    console.log(id, " ", container_id, " ", typeof container_id, " ", typeof id)
    document.getElementById(container_id).removeChild(document.getElementById(id));
    const current_facilities = selected_facilities.filter(p => p.id !== facility_id);
    console.log(current_facilities)
    selected_facilities = current_facilities;
    
    const canceled_facility=facilities.filter(p=>p.uid===facility_id)[0];
    choosed_facilities.push(canceled_facility);
    select_facility.innerHTML=`<option selected>Select Facilities</option>`;
    choosed_facilities.map((v)=>{
        select_facility.innerHTML += get_options_child(v.uid, v.facility_value)
    })
}

function render_facility_charge_inputs(facility, container) {

    const charge_id = Math.floor(new Date().getTime() / 1000);
    const penalty_charge_id = Math.floor(new Date().getTime() / 1000) + (Math.floor(Math.random() * (9999 - 1111 + 1)) + 1111);
    const main_div_id = Math.floor(new Date().getTime() / 1000) + (Math.floor(Math.random() * (9999 - 1111 + 1)) + 1111).toString();;

    // Create elements
    const facilityDiv = document.createElement('div');
    facilityDiv.id = main_div_id

    const facilityNameDiv = document.createElement('div');
    facilityNameDiv.classList.add('flex', 'items-center', 'justify-between', 'mt-3');
    facilityNameDiv.innerHTML = `
    <div class="flex justify-between w-full mt-3">
        <label class="block text-sm font-medium leading-6 text-gray-900">Facility Name</label>
        <i class="fa-solid fa-xmark cursor-pointer" onclick="canceled_facility('${main_div_id}','${container.id}','${facility.uid}')"></i>
    </div>
    `;

    const facilityInputDiv = document.createElement('div');
    facilityInputDiv.classList.add('mt-2');
    facilityInputDiv.innerHTML = `<input type="text" value="${facility.facility_value}" disabled
                 class="block p-2 w-full bg-gray-200 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">`;

    const chargeDiv = document.createElement('div');
    chargeDiv.classList.add('flex', 'items-center', 'justify-between');
    chargeDiv.innerHTML = `<label class="block text-sm font-medium leading-6 text-gray-900">Set Charge (Per hour)</label>`;

    const chargeInputDiv = document.createElement('div');
    chargeInputDiv.classList.add('mt-2');
    const chargeInput = document.createElement('input');
    chargeInput.setAttribute('type', 'text');
    chargeInput.setAttribute('placeholder', 'In Indian Rupees');
    chargeInput.setAttribute('id', charge_id);
    chargeInput.classList.add('block', 'p-2', 'w-full', 'rounded-md', 'border-0', 'py-1.5', 'text-gray-900', 'shadow-sm', 'ring-1', 'ring-inset', 'ring-gray-300', 'placeholder:text-gray-400', 'focus:ring-2', 'focus:ring-inset', 'focus:ring-indigo-600', 'sm:text-sm', 'sm:leading-6');
    chargeInput.addEventListener("input", () => {
        set_charges(facility.uid, charge_id, 'charge');
    })

    const penaltyDiv = document.createElement('div');
    penaltyDiv.classList.add('flex', 'items-center', 'justify-between');
    penaltyDiv.innerHTML = `<label class="block text-sm font-medium leading-6 text-gray-900">Set Penalty Charge (Per hour)</label>`;

    const penaltyInputDiv = document.createElement('div');
    penaltyInputDiv.classList.add('mt-2');
    const penaltyInput = document.createElement('input');
    penaltyInput.setAttribute('type', 'text');
    penaltyInput.setAttribute('placeholder', 'In Indian Rupees');
    penaltyInput.setAttribute('id', penalty_charge_id);
    penaltyInput.classList.add('block', 'p-2', 'w-full', 'rounded-md', 'border-0', 'py-1.5', 'text-gray-900', 'shadow-sm', 'ring-1', 'ring-inset', 'ring-gray-300', 'placeholder:text-gray-400', 'focus:ring-2', 'focus:ring-inset', 'focus:ring-indigo-600', 'sm:text-sm', 'sm:leading-6');
    penaltyInput.addEventListener("input", () => {
        set_charges(facility.uid, penalty_charge_id, 'penalty');
    })

    // Append elements
    facilityDiv.appendChild(facilityNameDiv);
    facilityDiv.appendChild(facilityInputDiv);
    facilityDiv.appendChild(chargeDiv);
    chargeInputDiv.appendChild(chargeInput);
    facilityDiv.appendChild(chargeInputDiv);
    facilityDiv.appendChild(penaltyDiv);
    penaltyInputDiv.appendChild(penaltyInput);
    facilityDiv.appendChild(penaltyInputDiv);

    container.appendChild(facilityDiv);
}

function get_facilities() {
    fetch("/admins/all-facilities")
        .then(res => res.json())
        .then(data => {
            facilities=[];
            choosed_facilities=[];
            select_facility.innerHTML=`<option selected>Select Facilities</option>`;
            JSON.parse(data.data)?.map(v => {
                let value = v.fields;
                facilities.push(value);
                choosed_facilities.push(value);
                select_facility.innerHTML += get_options_child(value.uid, value.facility_value)
            })
        })
}
get_facilities()

select_facility.addEventListener("change", () => {
    const facility_id = select_facility.value;
    const facility = facilities.filter(p => p.uid === facility_id)[0];
    const _remain_facilities = choosed_facilities.filter(p => p.uid !== facility_id);
    choosed_facilities=_remain_facilities;
    select_facility.innerHTML=`<option selected>Select Facilities</option>`;
    choosed_facilities.map((v)=>{
        select_facility.innerHTML += get_options_child(v.uid, v.facility_value)
    })
    render_facility_charge_inputs(facility, facility_container);
})

function create() {

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
    let text=create_btn.textContent;
    create_btn.disabled=true;
    create_btn.textContent='Loading...';

    fetch('/admins/parking-area', {
        method: "POST",
        body: JSON.stringify({ "facilities": selected_facilities, "area_name": area, "selected_days":_selected_days })
    })
        .then(res => res.json())
        .then(data => {
            setTimeout(() => {
                window.location.reload();
            }, 300)
        })
        .finally(()=>{
            create_btn.disabled=false;
            create_btn.textContent=text;
        })
}