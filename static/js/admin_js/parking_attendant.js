const attendatnt_modal_btn_container=document.getElementById("attendatnt-modal-btn-container");
const attendatnt_number_of_pagination=document.getElementById("attendatnt-number-of-pagination");
const attendant_table_body=document.getElementById("attendant-table-body");
const prev_btns=document.getElementById("prev");
const next_btns=document.getElementById("next");

const pagination_numbers = [20, 50, 100, 200]
let selected_pagination_number;
let page = 1;
let total_records=0;
let delete_confirmation_dialogue_btn;

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
    
    const button_delete_confirm = document.createElement("button");
    button_delete_confirm.type = "button";
    button_delete_confirm.setAttribute("data-modal-target", "area-delete-modal");
    button_delete_confirm.setAttribute("data-modal-toggle", "area-delete-modal");
    button_delete_confirm.classList.add("hidden");
    attendatnt_modal_btn_container.appendChild(button_delete_confirm);
    delete_confirmation_dialogue_btn=button_delete_confirm;
    
    pagination_numbers.map((v, i) => {
        const option = document.createElement("option");
        option.value = v;
        option.innerText = v;
        option.classList.add('attendant-table-paginate-options');
        if (i === 0) {
            if(getCookie('attendant_table_pagination_number')===null){
                selected_pagination_number = v;
                option.selected = true;
            }
        }
        attendatnt_number_of_pagination.appendChild(option);
    })

    if(getCookie('attendant_table_pagination_number')!==null){
        const attendant_table_pagination_number=getCookie('attendant_table_pagination_number');
        selected_pagination_number = attendant_table_pagination_number;
        const options = document.querySelectorAll('.attendant-table-paginate-options');
                options.forEach(element => {
                    if(element.value===attendant_table_pagination_number){
                        element.selected = true;
                    }
        });
    }

    get_parking_attendants(page, selected_pagination_number);
})

attendatnt_number_of_pagination.addEventListener("change", () => {
    selected_pagination_number = attendatnt_number_of_pagination.value;
    document.cookie=`attendant_table_pagination_number=${attendatnt_number_of_pagination.value}`
    get_parking_attendants(page,attendatnt_number_of_pagination.value);
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
    get_parking_attendants(pages,selected_pagination_number);
})

prev_btns.addEventListener("click",()=>{
    const pages=prev(page);
    page=pages;
    paginate_btn_handel(total_records,selected_pagination_number,pages);
    get_parking_attendants(pages,selected_pagination_number);
})

function verification_toggler(subadmin_id,input_id){
    const inp=document.getElementById(input_id);
    let verification=inp.checked;
    fetch('/admins/verify-attendant',{
        method:"POST",
        body:JSON.stringify({'attendant_id':subadmin_id})
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
    })
}

function suspended_toggler(subadmin_id,input_id){
    const inp=document.getElementById(input_id);
    let suspend=inp.checked;
    fetch('/admins/suspend-attendant',{
        method:"POST",
        body:JSON.stringify({'attendant_id':subadmin_id})
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
    })
}

function delete_attendant(subadmin_id,name){
    const area_delete_modal_context=document.getElementById("area-delete-modal-context");
    const area_delete_modal_submit=document.getElementById("area-delete-modal-submit");
    const close_btn=document.getElementById('area-delete-modal-close');
    area_delete_modal_context.innerText=`Are you sure you want to delete ${name}?`

    area_delete_modal_submit.addEventListener("click",()=>{
        fetch(`/admins/delete-parking-attendant/${subadmin_id}`,{
            method:'DELETE'
        })
        .then(res=>res.json())
        .then(data=>{
            if(data?.status===200){
                close_btn.click();
            }
        })
    })
    delete_confirmation_dialogue_btn.click();
}

const render_table_row=(subadmin_id,name,phone,email,areas,joined_at,is_verified,is_suspended)=>{
    const tr = document.createElement("tr");
    tr.classList.add("bg-gray-100");
    tr.classList.add("dark:bg-gray-100");

    const name_child=document.createElement("td");
    name_child.classList.add("px-6", "py-3");
    name_child.innerText = name;

    const phone_child=document.createElement("td");
    phone_child.classList.add("px-6", "py-3");
    phone_child.innerText = phone;

    const email_child=document.createElement("td");
    email_child.classList.add("px-6", "py-3");
    email_child.innerText = email;

    const areas_child=document.createElement("td");
    areas_child.classList.add("px-6", "py-3");
    areas_child.innerText = "Wait";

    const joined_at_child=document.createElement("td");
    joined_at_child.classList.add("px-6", "py-3");
    joined_at_child.innerText = new Date(joined_at).toLocaleDateString();

    const verified_child=document.createElement("td");
    verified_child.classList.add("px-6", "py-3");
    const toggle_verification_id=subadmin_id+Math.floor(Math.random() * 1000).toString();
    const toggle_verification_child=`
            <label class="inline-flex items-center cursor-pointer">
              <input id=${toggle_verification_id} ${is_verified ? 'checked' : ''} type="checkbox" value="" class="sr-only peer" onclick="verification_toggler('${subadmin_id}','${toggle_verification_id}')">
              <div class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
            </label>
            `
    verified_child.innerHTML=toggle_verification_child

    const suspended_child=document.createElement("td");
    verified_child.classList.add("px-6", "py-3");
    const toggle_suspended_id=subadmin_id+Math.floor(Math.random() * 2000).toString();
    const toggle_suspended_child=`
            <label class="inline-flex items-center cursor-pointer">
              <input id=${toggle_suspended_id} ${is_suspended ? 'checked' : ''} type="checkbox" value="" class="sr-only peer" onclick="suspended_toggler('${subadmin_id}','${toggle_suspended_id}')">
              <div class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
            </label>
            `
    suspended_child.innerHTML=toggle_suspended_child;

    const delete_child=document.createElement("td");
    delete_child.classList.add("px-6", "py-3");
    const delete_icon = document.createElement("i");
    delete_icon.classList.add("fa-solid", "fa-trash","cursor-pointer");
    delete_icon.style.fontSize="17px";
    delete_icon.addEventListener("click", function () {
        delete_attendant(subadmin_id,name);
    });
    delete_child.appendChild(delete_icon);

    tr.appendChild(name_child);
    tr.appendChild(phone_child);
    tr.appendChild(email_child);
    tr.appendChild(areas_child);
    tr.appendChild(joined_at_child);
    tr.appendChild(verified_child);
    tr.appendChild(suspended_child);
    tr.appendChild(delete_child);

    attendant_table_body.appendChild(tr);
}

const get_parking_attendants=(page,page_size)=>{
    fetch(`/admins/get-parking-attendants?page=${page}&page-size=${page_size}`)
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
        attendant_table_body.innerHTML="";
        data?.attached_subadmins?.map((v)=>{
            render_table_row(v.uid,v.name,v.phone,v.email,v.associate_areas,v.created_at,v.is_verified,v.is_suspended)
        })
        total_records=data.total_records;
        paginate_btn_handel(data.total_records,selected_pagination_number,page);
    })
}