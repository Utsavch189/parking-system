const number_of_pagination = document.getElementById("number-of-pagination");
const next_btns = document.getElementById("next");
const prev_btns = document.getElementById("prev");
const slot_table_body=document.getElementById("slot-table-body");

const modal_btn_container = document.getElementById("modal-btn-container");
const view_modal=document.getElementById("view-modal");
const slot_edit_modal=document.getElementById("edit-slot-modal");

const pagination_numbers = [20, 50, 100, 200]
let selected_pagination_number;
let page = 1;
let total_records=0;

let view_modal_btn;
let slot_edit_modal_btn;

// Edit Section
let radio_onchage_func;
const slot_edit_address_section=document.getElementById("slot-edit-address-section");
const edit_facility_section=document.getElementById("edit-facility-section");
const edit_timings_section=document.getElementById("edit-timings-section");
const update_slot_name_btn=document.getElementById("update-slot-name-btn");
const update_slot_facility_btn=document.getElementById("update-slot-facility-btn");
const update_slot_timings_btn=document.getElementById("update-slot-timings-btn");

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

    const view_modal_btns = document.createElement("button");
    view_modal_btns.type = "button";
    view_modal_btns.setAttribute("data-modal-target", "view-modal");
    view_modal_btns.setAttribute("data-modal-toggle", "view-modal");
    view_modal_btns.classList.add("hidden");
    modal_btn_container.appendChild(view_modal_btns);
    view_modal_btn = view_modal_btns;

    const slot_edit_modal_btns = document.createElement("button");
    slot_edit_modal_btns.type = "button";
    slot_edit_modal_btns.setAttribute("data-modal-target", "edit-slot-modal");
    slot_edit_modal_btns.setAttribute("data-modal-toggle", "edit-slot-modal");
    slot_edit_modal_btns.classList.add("hidden");
    modal_btn_container.appendChild(slot_edit_modal_btns);
    slot_edit_modal_btn = slot_edit_modal_btns;

    pagination_numbers.map((v, i) => {
        const option = document.createElement("option");
        option.value = v;
        option.innerText = v;
        option.classList.add('slot-table-paginate-options');
        if (i === 0) {
            if(getCookie('slot_table_pagination_number')===null){
                selected_pagination_number = v;
                option.selected = true;
            }
        }
        number_of_pagination.appendChild(option);
    })

    if(getCookie('slot_table_pagination_number')!==null){
        const slot_table_pagination_number=getCookie('slot_table_pagination_number');
        selected_pagination_number = slot_table_pagination_number;
        const options = document.querySelectorAll('.slot-table-paginate-options');
                options.forEach(element => {
                    if(element.value===slot_table_pagination_number){
                        element.selected = true;
                    }
        });
    }

    get_slots(page,selected_pagination_number);
})

number_of_pagination.addEventListener("change", () => {
    selected_pagination_number = number_of_pagination.value;
    document.cookie=`slot_table_pagination_number=${number_of_pagination.value}`
    get_slots(page,number_of_pagination.value);
})

function isLastPage(totalRecords, pageSize, currentPage) {
    const totalPages = Math.ceil(totalRecords / pageSize);
    return currentPage === totalPages;
}

const next = (currentPage) => currentPage + 1;

const prev = (currentPage) => (currentPage > 1 ? currentPage - 1 : currentPage);

const paginate_btn_handel = (totalRecords, selectedPaginationNumbers, currentPage) => {
    const isFirstPage = currentPage === 1;
    const lastPage = isLastPage(totalRecords, selectedPaginationNumbers, currentPage);

    if(totalRecords===0 && page===1){
        prev_btns.classList.add('bg-gray-400');
        prev_btns.setAttribute('disabled', true);
        next_btns.classList.add('bg-gray-400');
        next_btns.setAttribute('disabled', true);
        return;
    }

    // Handle Previous Button
    if (isFirstPage) {
        prev_btns.classList.add('bg-gray-400');
        prev_btns.setAttribute('disabled', true);
    } else {
        prev_btns.classList.remove('bg-gray-400');
        prev_btns.removeAttribute('disabled');
    }

    // Handle Next Button
    if (lastPage) {
        next_btns.classList.add('bg-gray-400');
        next_btns.setAttribute('disabled', true);
    } else {
        next_btns.classList.remove('bg-gray-400');
        next_btns.removeAttribute('disabled');
    }
}

next_btns.addEventListener("click", () => {
    const pages = next(page);
    page = pages;
    get_slots(page,selected_pagination_number);
});

prev_btns.addEventListener("click", () => {
    const pages = prev(page);
    page = pages;
    get_slots(page,selected_pagination_number);
});

function address_modal(address,type){
    document.getElementById('view-modal-heading').innerText=`Showing ${type}`;
    document.getElementById('view-modal-body').innerText=address;
    view_modal_btn.click()
}

function show_booking_qr(qr_link){

}

function view_facilities(facilities,slot_no){
    document.getElementById('view-modal-heading').innerText=`Showing Facilities For Slot ${slot_no}`;
    const table = `
        <table class="w-full text-sm text-center rtl:text-right text-black dark:text-black">
            <thead class="text-xs text-black uppercase bg-gray-50 dark:bg-gray-100 dark:text-black">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        Facility
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Charge (per hour)
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Penalty (per hour)
                    </th>
                </tr>
            </thead>
            <tbody>
                ${facilities?.map(v => `
                    <tr>
                        <td class="px-6 py-3">${v.facility.facility_value}</td>
                        <td class="px-6 py-3">${"N/A"}</td>
                        <td class="px-6 py-3">${"N/A"}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    document.getElementById('view-modal-body').innerHTML=table;
    view_modal_btn.click()
}

function view_timings(timings,slot_no){
    document.getElementById('view-modal-heading').innerText=`Showing Timings For Slot ${slot_no}`;
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
    document.getElementById('view-modal-body').innerHTML=table;
    view_modal_btn.click()
}

function edit_slot(slot_id,slot_no,facilities,timings,address,direction_guidance){
    document.getElementById('edit-slot-modal-heading').innerText=`Edit Slot ${slot_no}`
    slot_edit_modal_btn.click()
}

function delete_slot(slot_id){

}

function render_slot(slot_id,slot_no,address,direction_guidance,booking_qr,facilities,timings,created_at){
    const tr = document.createElement("tr");
    tr.classList.add("bg-gray-100");
    tr.classList.add("dark:bg-gray-100");

    const slot_no_child= document.createElement("td");
    slot_no_child.classList.add("px-6", "py-3");
    slot_no_child.innerText = slot_no;

    const address_child = document.createElement("td");
    address_child.classList.add("px-6", "py-3");
    const address_child_icon=document.createElement("i");
    address_child_icon.classList.add("fa-solid", "fa-location-dot", "cursor-pointer")
    address_child_icon.addEventListener("click",()=>{
        address_modal(address,'Address');
    })
    address_child.appendChild(address_child_icon);

    const direction_child = document.createElement("td");
    direction_child.classList.add("px-6", "py-3");
    const direction_child_icon=document.createElement("i");
    direction_child_icon.classList.add("fa-solid", "fa-compass", "cursor-pointer")
    direction_child_icon.addEventListener("click",()=>{
        address_modal(direction_guidance,'Direction Guidance');
    })
    direction_child.appendChild(direction_child_icon);

    const booking_qr_child = document.createElement("td");
    booking_qr_child.classList.add("px-6", "py-3");
    const booking_qr_child_icon=document.createElement("i");
    booking_qr_child_icon.classList.add("fa-solid", "fa-qrcode", "cursor-pointer")
    booking_qr_child_icon.addEventListener("click",()=>{
        show_booking_qr(booking_qr);
    })
    booking_qr_child.appendChild(booking_qr_child_icon);

    const facilities_child = document.createElement("td");
    facilities_child.classList.add("px-6", "py-3");
    const icon = document.createElement("i");
    icon.classList.add("fa-solid", "fa-circle-info", "cursor-pointer");
    icon.addEventListener("click", function () {
        view_facilities(facilities,slot_no);
    });
    facilities_child.appendChild(icon);

    const timings_child = document.createElement("td");
    timings_child.classList.add("px-6", "py-3");
    const clock_icon = document.createElement("i");
    clock_icon.classList.add("fa-solid", "fa-clock", "cursor-pointer");
    clock_icon.addEventListener("click", function () {
        view_timings(timings,slot_no);
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
        edit_slot(slot_id,slot_no,facilities,timings,address,direction_guidance);
    });
    edit_child.appendChild(edit_icon);


    const delete_child=document.createElement("td");
    delete_child.classList.add("px-6", "py-3");
    const delete_icon = document.createElement("i");
    delete_icon.classList.add("fa-solid", "fa-trash","cursor-pointer");
    delete_icon.addEventListener("click", function () {
        delete_slot(slot_id);
    });
    delete_child.appendChild(delete_icon);

    tr.appendChild(slot_no_child);
    tr.appendChild(address_child);
    tr.appendChild(direction_child);
    tr.appendChild(booking_qr_child);
    tr.appendChild(facilities_child);
    tr.appendChild(timings_child);
    tr.appendChild(created_at_child);
    tr.appendChild(edit_child);
    tr.appendChild(delete_child);

    slot_table_body.appendChild(tr);
}

function get_slots(page,page_size){
    fetch(`/parking-owner/parking-slot?page=${page}&page-size=${page_size}`)
    .then(res=>res.json())
    .then(data=>{
        total_records=data?.total_records ? data.total_records : 0
        slot_table_body.innerHTML="";
        data?.slots?.length>0 && data?.slots?.map(v=>{
            render_slot(v.uid,v.slot_no,v.address,v.direction_guidance,v.slot_booking_qr,v.facilities,v.timings,v.created_at)
        })
        paginate_btn_handel(total_records,selected_pagination_number,page);
    })
}