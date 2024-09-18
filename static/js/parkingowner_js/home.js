const number_of_pagination = document.getElementById("number-of-pagination");
const next_btns = document.getElementById("next");
const prev_btns = document.getElementById("prev");

const pagination_numbers = [20, 50, 100, 200]
let selected_pagination_number;
let page = 1;
let total_records=0;

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

    paginate_btn_handel(total_records,selected_pagination_number,page);
})

number_of_pagination.addEventListener("change", () => {
    selected_pagination_number = number_of_pagination.value;
    document.cookie=`slot_table_pagination_number=${number_of_pagination.value}`
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
    paginate_btn_handel(total_records, selected_pagination_number, pages);
});

prev_btns.addEventListener("click", () => {
    const pages = prev(page);
    page = pages;
    paginate_btn_handel(total_records, selected_pagination_number, pages);
});