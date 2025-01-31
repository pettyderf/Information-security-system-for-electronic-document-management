
function autenrificate() {
    let login = document.getElementById("username").value;
    let pass = document.getElementById("password").value;
    
}

function open_registration() {
    window.open("registr.html", "_self");
}

// function registration() {
//     let login = document.getElementById("new_username").value;
//     let pass_1 = document.getElementById("password_1").value;
//     let pass_2 = document.getElementById("password_2").value;
//     let hash_pass_1 = JSON.stringify(CryptoJS.SHA256(pass_1));
//     let hash_pass_2 = JSON.stringify(CryptoJS.SHA256(pass_2));
//     if (hash_pass_1 != hash_pass_2) {
//         alert("Пароли не совпадают.")
//     } else {
//         let hash_log = JSON.stringify(CryptoJS.SHA256(login)["words"]);
//         let hash_pass = JSON.stringify(CryptoJS.SHA256(pass_1)["words"]);
//         document.getElementById('h_login').innerHTML = hash_log;
//         document.getElementById('h_pass').innerHTML = hash_pass;
//     }
// }
