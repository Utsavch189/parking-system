const number_of_pagination = document.getElementById("number-of-pagination");
const next_btns = document.getElementById("next");
const prev_btns = document.getElementById("prev");
const area_table_body = document.getElementById("area-table-body");
const view_facilities_modal = document.getElementById("view-facilities-modal");
const view_timings_modal=document.getElementById("view-timings-modal");
const edit_parking_modal=document.getElementById("edit-parking-modal");
const qr_modal=document.getElementById('qr-modal');
const modal_btn_container = document.getElementById("modal-btn-container");

const pagination_numbers = [20, 50, 100, 200]
let selected_pagination_number;
let page = 1;
let view_facilities_modal_btn;
let view_timings_modal_btn;
let edit_parking_modal_btn;
let qr_modal_btn;
let delete_confirmation_dialogue_btn;
let total_records=0;

// Edit Modal
let facilities_for_edit=[];
let selected_facilities_for_edit=[];
let all_facilities = [];
let select_tag_rendered_facilities=[];
let updated_facilities=[];
let selected_edited_days=[];
let updated_area_name="";
let area_id="";
const update_area_name_btn=document.getElementById('update-area-name-btn');
const update_area_facility_btn=document.getElementById('update-area-facility-btn');
const update_area_timings_btn=document.getElementById('update-area-timings-btn');

let radio_onchage_func;

function getCookie(name) {
    const cookieString = document.cookie;
    const cookies = cookieString.split('; ');
    
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const [cookieName, cookieValue] = cookie.split('=');
        
        if (cookieName === name) {
            return cookieValue;
        }
    }
    
    return null;
}

document.addEventListener("DOMContentLoaded", () => {
    const facility_view_button = document.createElement("button");
    facility_view_button.type = "button";
    facility_view_button.setAttribute("data-modal-target", "view-facilities-modal");
    facility_view_button.setAttribute("data-modal-toggle", "view-facilities-modal");
    facility_view_button.classList.add("hidden");
    modal_btn_container.appendChild(facility_view_button);
    view_facilities_modal_btn = facility_view_button;

    const timing_view_button = document.createElement("button");
    timing_view_button.type = "button";
    timing_view_button.setAttribute("data-modal-target", "view-timings-modal");
    timing_view_button.setAttribute("data-modal-toggle", "view-timings-modal");
    timing_view_button.classList.add("hidden");
    modal_btn_container.appendChild(timing_view_button);
    view_timings_modal_btn = timing_view_button;

    const edit_modal_btns = document.createElement("button");
    edit_modal_btns.type = "button";
    edit_modal_btns.setAttribute("data-modal-target", "edit-parking-modal");
    edit_modal_btns.setAttribute("data-modal-toggle", "edit-parking-modal");
    edit_modal_btns.classList.add("hidden");
    modal_btn_container.appendChild(edit_modal_btns);
    edit_parking_modal_btn = edit_modal_btns;

    const qr_modal_btns = document.createElement("button");
    qr_modal_btns.type = "button";
    qr_modal_btns.setAttribute("data-modal-target", "qr-modal");
    qr_modal_btns.setAttribute("data-modal-toggle", "qr-modal");
    qr_modal_btns.classList.add("hidden");
    modal_btn_container.appendChild(qr_modal_btns);
    qr_modal_btn = qr_modal_btns;

    const button_delete_confirm = document.createElement("button");
    button_delete_confirm.type = "button";
    button_delete_confirm.setAttribute("data-modal-target", "area-delete-modal");
    button_delete_confirm.setAttribute("data-modal-toggle", "area-delete-modal");
    button_delete_confirm.classList.add("hidden");
    modal_btn_container.appendChild(button_delete_confirm);
    delete_confirmation_dialogue_btn=button_delete_confirm;

    pagination_numbers.map((v, i) => {
        const option = document.createElement("option");
        option.value = v;
        option.innerText = v;
        option.classList.add('area-table-paginate-options');
        if (i === 0) {
            if(getCookie('area_table_pagination_number')===null){
                selected_pagination_number = v;
                option.selected = true;
            }
        }
        number_of_pagination.appendChild(option);
    })

    if(getCookie('area_table_pagination_number')!==null){
        const area_table_pagination_number=getCookie('area_table_pagination_number');
        selected_pagination_number = area_table_pagination_number;
        const options = document.querySelectorAll('.area-table-paginate-options');
                options.forEach(element => {
                    if(element.value===area_table_pagination_number){
                        element.selected = true;
                    }
        });
    }

    get_data(page, selected_pagination_number);
})

number_of_pagination.addEventListener("change", () => {
    selected_pagination_number = number_of_pagination.value;
    document.cookie=`area_table_pagination_number=${number_of_pagination.value}`
    get_data(page,number_of_pagination.value);
})

function isLastPage(totalRecords, pageSize, currentPage) {
    const totalPages = Math.ceil(totalRecords / pageSize);
    return currentPage === totalPages;
}

const next = (currentPage) => {
    const pages=currentPage + 1;
    return pages;
}

const prev = (currentPage) => {
    if (currentPage === 1) {
        return currentPage;
    }
    const pages= currentPage - 1;
    return pages;
}

const paginate_btn_handel=(total_recordss,selected_pagination_numbers,pages)=>{
    if (pages === 1 && isLastPage(total_recordss, selected_pagination_numbers, pages)) {
        prev_btns.classList.add('bg-gray-400');
        prev_btns.setAttribute('disabled', true);
        next_btns.classList.add('bg-gray-400');
        next_btns.setAttribute('disabled', true);
    }

    else if(isLastPage(total_recordss,selected_pagination_numbers,pages)){
        next_btns.classList.add('bg-gray-400');
        next_btns.setAttribute('disabled', true);
        prev_btns.classList.remove('bg-gray-400');
        prev_btns.removeAttribute('disabled');
        page=1;
    }
    
    else if(pages===1 && !isLastPage(total_recordss, selected_pagination_numbers, pages)){
        prev_btns.classList.add('bg-gray-400');
        prev_btns.setAttribute('disabled', true);
        next_btns.classList.remove('bg-gray-400');
        next_btns.removeAttribute('disabled');
    }
    else{
        next_btns.classList.remove('bg-gray-400');
        next_btns.removeAttribute('disabled');
        prev_btns.classList.remove('bg-gray-400');
        prev_btns.removeAttribute('disabled');
    }
}

next_btns.addEventListener("click",()=>{
    const pages=next(page);
    page=pages;
    paginate_btn_handel(total_records,selected_pagination_number,pages);
    get_data(pages,selected_pagination_number);
})

prev_btns.addEventListener("click",()=>{
    const pages=prev(page);
    page=pages;
    paginate_btn_handel(total_records,selected_pagination_number,pages);
    get_data(pages,selected_pagination_number);
})

const view_facilities = (facilitiess,area_name) => {
    if (view_facilities_modal && view_facilities_modal_btn) {
        const view_facilities_modal_body = document.getElementById("view-facilities-modal-body");
        view_facilities_modal_body.innerHTML = "";
        
        const view_facilities_modal_heading=document.getElementById("view-facilities-modal-heading");
        view_facilities_modal_heading.innerText=`View Facilities For ${area_name}`;

        facilitiess?.length > 0 && facilitiess.map((v, i) => {
            const inp_grp = `
            <div class="mt-3">
                <label class="block text-xl font-medium leading-6 text-gray-900">Facility-${i+1}</label>
                <div class="flex flex-col items-start justify-between mt-3"> 
                    <label class="block text-sm font-medium leading-6 text-gray-900">Facility Type</label>
                    <input type="text" value="${v.facility.facility_name}" disabled
                        class="block p-2 w-full bg-gray-200 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                </div>
               
               <div class="flex flex-col items-start justify-between mt-3"> 
                    <label class="block text-sm font-medium leading-6 text-gray-900">Facility Name</label>
                    <input type="text" value="${v.facility.facility_value}" disabled
                        class="block p-2 w-full bg-gray-200 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
               </div> 

               <div class="flex flex-col items-start justify-between mt-3"> 
                    <label class="block text-sm font-medium leading-6 text-gray-900">Charge (Per hour)</label>
                    <input type="text" value="${v.charges}" disabled
                        class="block p-2 w-full bg-gray-200 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
               </div>

               <div class="flex flex-col items-start justify-between mt-3"> 
                    <label class="block text-sm font-medium leading-6 text-gray-900">Penalty Charge (Per hour)</label>
                    <input type="text" value="${v.penalty_charge_per_hour}" disabled
                        class="block p-2 w-full bg-gray-200 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
               </div>
            </div>
            `
            view_facilities_modal_body.innerHTML += inp_grp;
        })
        view_facilities_modal_btn.click();
    }
}

function view_timings(timings, area_name) {
    const body = document.getElementById('view-timings-modal-body');
    body.innerHTML = "";
    const heading = document.getElementById("view-timing-modal-heading");
    heading.innerText = `View Timings For ${area_name}`;
    
    const table = `
        <table class="w-full text-sm text-center rtl:text-right text-black dark:text-black">
            <thead class="text-xs text-black uppercase bg-gray-50 dark:bg-gray-100 dark:text-black">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        Day
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Opening Time
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Closing Time
                    </th>
                </tr>
            </thead>
            <tbody>
                ${timings.map(v => `
                    <tr>
                        <td class="px-6 py-3">${v.day}</td>
                        <td class="px-6 py-3">${v.open_time}</td>
                        <td class="px-6 py-3">${v.close_time}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    body.innerHTML = table;
    view_timings_modal_btn.click();
}

function delete_area(area_id,area_name){
    const area_delete_modal_context=document.getElementById("area-delete-modal-context");
    const area_delete_modal_submit=document.getElementById("area-delete-modal-submit");
    area_delete_modal_context.innerText=`Are you sure you want to delete area ${area_name}?`
    delete_confirmation_dialogue_btn.click()
    area_delete_modal_submit.addEventListener("click",()=>{
        fetch(`/admins/delete-parking-area/${area_id}`,{
            method:"DELETE"
        })
        .then(res=>res.json())
        .then(data=>{
            if(data?.status===200){
                document.getElementById('area-delete-modal-close').click();
            }
        })
    })
    
}

const get_remain_facilities_after_choosing=(_all_facilities,_facilitiesss)=>{
    updated_facilities=[];

    for(let i=0;i<_all_facilities.length;i++){
        const exists=_facilitiesss.filter(p=>p['facility'].uid===_all_facilities[i].uid);
        if(!exists.length){
            updated_facilities.push(_all_facilities[i]);
        }
    }
}

function set_charge(facility_id, input_id, charge_type) {
    if (charge_type === 'charge') {
        var charge_inp_id = input_id.toString();
        let facility = selected_facilities_for_edit.filter(p => p.id === facility_id);
        if (!facility.length) {
            const facility_obj = {
                id: facility_id,
                charges: document.getElementById(charge_inp_id).value,
                penalty_charge_per_hour: null
            };
            selected_facilities_for_edit.push(facility_obj);
        }
        else {
            facility[0]['charges'] = document.getElementById(charge_inp_id).value;
        }
    }
    else if (charge_type === 'penalty') {
        var penalty_charge_inp_id = input_id.toString();
        let facility = selected_facilities_for_edit.filter(p => p.id === facility_id);
        if (!facility.length) {
            const facility_obj = {
                id: facility_id,
                charges: null,
                penalty_charge_per_hour: document.getElementById(penalty_charge_inp_id).value
            };
            selected_facilities_for_edit.push(facility_obj);
        }
        else {
            facility[0]['penalty_charge_per_hour'] = document.getElementById(penalty_charge_inp_id).value;
        }
    }
}

function cancel_facility(id, container_id, facility_id,uid="") {
    const current_facilities_charges = selected_facilities_for_edit.filter(p => p.id !== facility_id);
    selected_facilities_for_edit=current_facilities_charges;
    
    if(uid!==""){
        const current_facilities=facilities_for_edit.filter(p=>p.uid!==uid);
        facilities_for_edit=current_facilities;

        get_remain_facilities_after_choosing(all_facilities,facilities_for_edit);
        document.getElementById('edit-facilities').innerHTML=`<option selected>Select Facilities</option>`;
        updated_facilities.map((v)=>{
            document.getElementById('edit-facilities').innerHTML+=`<option value=${v.uid}>${v.facility_value}</option>`
        })
    }
    else{
        const canceled_facility=all_facilities.filter(p=>p.uid===facility_id)[0];
        updated_facilities.push(canceled_facility);
        document.getElementById('edit-facilities').innerHTML=`<option selected>Select Facilities</option>`;
        updated_facilities.map((v)=>{
            document.getElementById('edit-facilities').innerHTML+=`<option value=${v.uid}>${v.facility_value}</option>`
        })
    }
    document.getElementById(container_id).removeChild(document.getElementById(id));
}

function render_facility_charge_inputs_for_edit(facility,container,uid="",charges_value="",penalty_chrages_value="") {
    const charge_id = Math.floor(new Date().getTime() / 1000) + (Math.floor(Math.random() * (9999 - 2222 + 1)) + 2222);;
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
        <i class="fa-solid fa-xmark cursor-pointer" onclick="cancel_facility('${main_div_id}','${container.id}','${facility.uid}','${uid}')"></i>
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
    chargeInput.value=charges_value
    chargeInput.classList.add('block', 'p-2', 'w-full', 'rounded-md', 'border-0', 'py-1.5', 'text-gray-900', 'shadow-sm', 'ring-1', 'ring-inset', 'ring-gray-300', 'placeholder:text-gray-400', 'focus:ring-2', 'focus:ring-inset', 'focus:ring-indigo-600', 'sm:text-sm', 'sm:leading-6');
    chargeInput.addEventListener("input", () => {
        set_charge(facility.uid, charge_id, 'charge');
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
    penaltyInput.value=penalty_chrages_value;
    penaltyInput.classList.add('block', 'p-2', 'w-full', 'rounded-md', 'border-0', 'py-1.5', 'text-gray-900', 'shadow-sm', 'ring-1', 'ring-inset', 'ring-gray-300', 'placeholder:text-gray-400', 'focus:ring-2', 'focus:ring-inset', 'focus:ring-indigo-600', 'sm:text-sm', 'sm:leading-6');
    penaltyInput.addEventListener("input", () => {
        set_charge(facility.uid, penalty_charge_id, 'penalty');
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

function update_area_name(){
    if (!updated_area_name) {
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
    fetch('/admins/parking-area', {
        method: "PUT",
        body: JSON.stringify({ "area_name": updated_area_name,"area_id":area_id })
    })
    .then(res => res.json())
    .then(data => {})
}

function update_area_facility(){
    let f=false;
    if (!selected_facilities_for_edit.length) {
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
    selected_facilities_for_edit.map((v) => {
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
    fetch('/admins/parking-area', {
        method: "PUT",
        body: JSON.stringify({ "facilities": selected_facilities_for_edit,"area_id":area_id })
    })
    .then(res => res.json())
    .then(data => {})
}

function update_area_timings(){
    let _selected_days=selected_edited_days.filter(p=>p.checked===true);
    console.log("selected_edited_days filtered : ",_selected_days)
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
    fetch('/admins/parking-area', {
        method: "PUT",
        body: JSON.stringify({ "selected_days": _selected_days,"area_id":area_id })
    })
    .then(res => res.json())
    .then(data => {})
}

function edit_area(facilitiess,timings,area_name,id){
    
    area_id="";
    area_id=id;

    const modal_heading=document.getElementById('edit-parking-modal-heading');
    modal_heading.innerText=`Edit Area ${area_name}`
    
    facilities_for_edit=[]
    facilities_for_edit=[...facilitiess];

    let _timings=[...timings];
    

    const edit_area_name_section=document.getElementById('edit_area_name_section');
    const edit_area_facilities_section=document.getElementById('edit-facility-section');
    let edit_area_timings_section=document.getElementById('edit_area_timings_section');

    let edit_area_name_inp=document.getElementById('edit-area-name');
    edit_area_name_inp.value=area_name;

    all_facilities=[];
    selected_facilities_for_edit=[];
    updated_area_name="";
    updated_area_name=area_name;

    fetch("/admins/all-facilities")
        .then(res => res.json())
        .then(data => {
            JSON.parse(data.data)?.map(v => {
                let value = v.fields;
                all_facilities.push(value);
            })
        })

    edit_area_name_inp.addEventListener("input",(e)=>{
        updated_area_name=e.target.value
    })
  
    radio_onchage_func=function(e){
        const element=e.target;
        if(element.id==="area_name_radio"){
            edit_area_name_section.classList.remove('hidden');
            edit_area_facilities_section.classList.add('hidden');
            edit_area_timings_section.classList.add('hidden');

            update_area_name_btn.classList.remove("hidden");
            update_area_facility_btn.classList.add("hidden");
            update_area_timings_btn.classList.add("hidden");

            edit_area_name_inp.value=updated_area_name!=="" ? updated_area_name : area_name;
        }
        else if(element.id==="area_facilities_radio"){
            edit_area_name_section.classList.add('hidden');
            edit_area_facilities_section.classList.remove('hidden');
            edit_area_timings_section.classList.add('hidden');

            update_area_name_btn.classList.add("hidden");
            update_area_facility_btn.classList.remove("hidden");
            update_area_timings_btn.classList.add("hidden");

            get_remain_facilities_after_choosing(all_facilities,facilities_for_edit);
            document.getElementById('edit-facilities').innerHTML=`<option selected>Select Facilities</option>`;
            updated_facilities.map((v)=>{
                document.getElementById('edit-facilities').innerHTML+=`<option value=${v.uid}>${v.facility_value}</option>`
            })
            const edit_facility_container=document.getElementById("edit-facility-container");
            edit_facility_container.innerHTML="";
            facilities_for_edit.map((v)=>{
                render_facility_charge_inputs_for_edit(v.facility,edit_facility_container,v.uid,v.charges,v.penalty_charge_per_hour);
                const is_exits=selected_facilities_for_edit.filter(p=>p.id===v.uid);
                if(!is_exits.length){
                    const charges_obj={
                        uid:v.uid,
                        id: v.facility.uid,
                        charges: v.charges,
                        penalty_charge_per_hour: v.penalty_charge_per_hour
                    }
                    selected_facilities_for_edit.push(charges_obj);
                }
            })

            document.getElementById('edit-facilities').addEventListener("change", () => {
                const facility_id = document.getElementById('edit-facilities').value;
                const facility = all_facilities.filter(p => p.uid === facility_id)[0];
                const current_facilities=updated_facilities.filter(p=>p.uid!==facility.uid);
                updated_facilities=current_facilities;
                document.getElementById('edit-facilities').innerHTML=`<option selected>Select Facilities</option>`;
                updated_facilities.map((v)=>{
                    document.getElementById('edit-facilities').innerHTML+=`<option value=${v.uid}>${v.facility_value}</option>`
                })
                render_facility_charge_inputs_for_edit(facility, edit_facility_container);
                const obj={
                        id: facility.uid,
                        charges: null,
                        penalty_charge_per_hour: null
                }
                selected_facilities_for_edit.push(obj);
            })
        }
        else if(element.id==="area_timings_radio"){
            edit_area_name_section.classList.add('hidden');
            edit_area_facilities_section.classList.add('hidden');
            edit_area_timings_section.classList.remove('hidden');

            update_area_name_btn.classList.add("hidden");
            update_area_facility_btn.classList.add("hidden");
            update_area_timings_btn.classList.remove("hidden");
            const dayss = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"];
    
            edit_area_timings_section.innerHTML="";

            dayss.forEach((v, i) => {
                const elm = `
                    <div class="mb-6">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center min-w-[4rem]">
                                <input id="${v+""+v}" name="days${i}" type="checkbox" value="${v}"
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
                                    <input type="time" id="start-${v+""+v}" name="start-${v}${i}"
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
                                    <input type="time" id="end-${v+""+v}" name="end-${v}${i}"
                                        class="bg-gray-50 ends-time border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                        min="09:00" max="18:00" value="00:00" required />
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                edit_area_timings_section.innerHTML += elm;
            });
        
            dayss.forEach((v) => {
                const checkbox = document.getElementById(v+""+v);
                const startTimeInput = document.getElementById(`start-${v+""+v}`);
                const endTimeInput = document.getElementById(`end-${v+""+v}`);
        
                if (checkbox) {
                    checkbox.addEventListener("input", () => {
                        console.log(`Checkbox ${v} value changed`);
                        const _day=selected_edited_days.filter(p=>p.day===v);
                        if(_day.length>0){
                            _day[0]['checked']===true ?_day[0]['checked']=false:_day[0]['checked']=true;
                        }
                        else{
                            if(startTimeInput?.value!=="00:00" && endTimeInput?.value==="00:00"){
                                let obj={
                                    "uid":null,
                                    "day":v,
                                    "open_time":startTimeInput.value,
                                    "close_time":null,
                                    "checked":true
                                }
                                selected_edited_days.push(obj);
                            }
                            else if(endTimeInput?.value!=="00:00" && startTimeInput?.value==="00:00"){
                                let obj={
                                    "uid":null,
                                    "day":v,
                                    "open_time":null,
                                    "close_time":endTimeInput?.value,
                                    "checked":true
                                }
                                selected_edited_days.push(obj);
                            }
                            else if(startTimeInput?.value!=="00:00" && endTimeInput?.value!=="00:00"){
                                let obj={
                                    "uid":null,
                                    "day":v,
                                    "open_time":startTimeInput.value,
                                    "close_time":endTimeInput.value,
                                    "checked":true
                                }
                                selected_edited_days.push(obj);
                            }
                            else{
                                let obj={
                                    "uid":null,
                                    "day":v,
                                    "open_time":null,
                                    "close_time":null,
                                    "checked":true
                                }
                                selected_edited_days.push(obj);
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
                        })
                        const _day=selected_edited_days.filter(p=>p.day===v);
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
                            }
                        })
                        const _day=selected_edited_days.filter(p=>p.day===v);
                        if(_day.length>0){
                            _day[0]['close_time']=endTimeInput.value;
                        }
                    });
                }
            });
            if(_timings.length){
                _timings.map((t,i)=>{
                    dayss.forEach((v) => {
                        if(t.day===v){
                            const checkbox = document.getElementById(v+""+v);
                            const startTimeInput = document.getElementById(`start-${v+""+v}`);
                            const endTimeInput = document.getElementById(`end-${v+""+v}`);

                            checkbox.setAttribute('checked',true);
                            startTimeInput.value=t.open_time;
                            endTimeInput.value=t.close_time;
                            let obj={
                                "uid":t.uid,
                                "day":v,
                                "open_time":t.open_time,
                                "close_time":t.close_time,
                                "checked":true
                            }
                            selected_edited_days.push(obj);
                        }
                    });
                })
            }
        }
    }
    document.querySelectorAll('.edit-radios').forEach((radio) => {
        radio.addEventListener('change', radio_onchage_func);
    });
    edit_parking_modal_btn.click()
}

function show_qr(url,area_name,type){

    let heading = type === 'searching' 
                ? `Slot Searching QR for Area ${area_name}`
                : type === 'register' 
                  ? `ParkingOwner Register QR for Area ${area_name}`
                  : '';
    document.getElementById('qr-modal-heading').innerText=heading;
    document.getElementById('qr-modal-body').innerHTML=`
        <div style="display:flex;flex-direction:column;justify-content:center;align-items:center">
            <img src='${url}' style="height:400px;width:400px"/>
            <div style="display:flex;gap:8px">
                <a class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" href="https://wa.me/?text=${url}" target="_blank">Share on WhatsApp</a>
            </div>
        </div>
    `;
    qr_modal_btn.click()
}

const render_table_body = (body_container, area_name, register_qr, searching_qr, facilitiess,timings, created_at,area_id) => {
    const tr = document.createElement("tr");
    tr.classList.add("bg-gray-100");
    tr.classList.add("dark:bg-gray-100");

    const area_name_child = document.createElement("td");
    area_name_child.classList.add("px-6", "py-3");
    area_name_child.innerText = area_name;

    const register_qr_child = document.createElement("td");
    register_qr_child.classList.add("px-6", "py-3");
    const register_qr_icon=document.createElement("i");
    register_qr_icon.classList.add("fa-solid", "fa-eye", "cursor-pointer")
    register_qr_icon.addEventListener("click",()=>{
        show_qr(register_qr,area_name,'register');
    })
    register_qr_child.appendChild(register_qr_icon);

    const searching_qr_child = document.createElement("td");
    searching_qr_child.classList.add("px-6", "py-3");
    const searching_qr_icon=document.createElement("i");
    searching_qr_icon.classList.add("fa-solid", "fa-eye", "cursor-pointer")
    searching_qr_icon.addEventListener("click",()=>{
        show_qr(searching_qr,area_name,'searching');
    })
    searching_qr_child.appendChild(searching_qr_icon);

    const facilities_child = document.createElement("td");
    facilities_child.classList.add("px-6", "py-3");
    const icon = document.createElement("i");
    icon.classList.add("fa-solid", "fa-circle-info", "cursor-pointer");
    icon.addEventListener("click", function () {
        view_facilities(facilitiess,area_name);
    });
    facilities_child.appendChild(icon);

    const timings_child = document.createElement("td");
    timings_child.classList.add("px-6", "py-3");
    const clock_icon = document.createElement("i");
    clock_icon.classList.add("fa-solid", "fa-clock", "cursor-pointer");
    clock_icon.addEventListener("click", function () {
        view_timings(timings,area_name);
    });
    timings_child.appendChild(clock_icon);

    const created_at_child = document.createElement("td");
    created_at_child.classList.add("px-6", "py-3");
    created_at_child.innerText = new Date(created_at).toLocaleDateString();

    const edit_child=document.createElement("td");
    edit_child.classList.add("px-6", "py-3");
    const edit_icon = document.createElement("i");
    edit_icon.classList.add("fa-solid", "fa-pen-to-square","cursor-pointer");
    edit_icon.addEventListener("click", function () {
        edit_area(facilitiess,timings,area_name,area_id);
    });
    edit_child.appendChild(edit_icon);


    const delete_child=document.createElement("td");
    delete_child.classList.add("px-6", "py-3");
    const delete_icon = document.createElement("i");
    delete_icon.classList.add("fa-solid", "fa-trash","cursor-pointer");
    delete_icon.addEventListener("click", function () {
        delete_area(area_id,area_name);
    });
    delete_child.appendChild(delete_icon);

    tr.appendChild(area_name_child);
    tr.appendChild(register_qr_child);
    tr.appendChild(searching_qr_child);
    tr.appendChild(facilities_child);
    tr.appendChild(timings_child);
    tr.appendChild(created_at_child);
    tr.appendChild(edit_child);
    tr.appendChild(delete_child);

    body_container.appendChild(tr);
}

const get_data = (page, page_size) => {
    fetch(`/admins/get-parking-areas?page=${page}&page-size=${page_size}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === 200) {
                area_table_body.innerHTML = "";
                data?.areas?.length > 0 && data?.areas.map((v) => {
                    render_table_body(
                        area_table_body,
                        v.area_name,
                        v.parking_owner_register_qr,
                        v.searchingslots_qr,
                        v.facilities,
                        v.timings,
                        v.created_at,
                        v.uid
                    )
                })
                total_records=data.total_records;
                paginate_btn_handel(data.total_records,selected_pagination_number,page);
            }
            
        })
}