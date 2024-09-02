export function validatePasswordLength(password, length) {
    if (password.length < length || password.length > length) {
        $.toast({
            text: `Password must be ${length} character long!`,
            showHideTransition: 'slide',
            bgColor: 'red',
            textColor: 'white',
            allowToastClose: true,
            hideAfter: 1000,
            stack: 5,
            textAlign: 'left',
            position: 'top-left'
        })
        return false
    }
    return true;
}

export function login(e,login_url,redirect_url,email_inp,password_inp) {
    if (e) {
        e.preventDefault()
    }
    const email = email_inp.value;
    const password = password_inp.value;

    const res = validatePasswordLength(password, 5);

    if (res) {
        fetch(login_url, {
            method: "POST",
            body: JSON.stringify({ "email": email, "password": password }),
            credentials: 'include'
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 200) {
                    window.location.replace(redirect_url);

                }
            })
            .catch(err => console.log(err))
    }
}

export function email_validate(email){
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email)
}