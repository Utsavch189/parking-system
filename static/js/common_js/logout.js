function logout(redirect_url){
    fetch("/auth/logout",{
        method:"POST",
        credentials: 'include'
    })
    .then(res=>res.json())
    .then(data=>{
        window.location.replace(redirect_url);
    })
    .catch(err=>console.log(err))
}