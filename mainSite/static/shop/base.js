// search_input = document.querySelector('#search_input')



// search_input.addEventListener("keyup", function(event) {
//     if (event.key === "Enter") {
//         event.preventDefault();
//         search();
//     }
// });

function validateSearch() {
    var searchInput = document.getElementById("search_input").value;
    if (searchInput.trim() === "") {
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}

var account_info = document.getElementById("accountinfo");
var is_account_info = false;
function account_info_show() {
    if (account_info.style.display === "none") {
        is_account_info=true;
        account_info.style.display = "block";
    }
}
$(document).click((event) => {
    if (is_account_info) {
        is_account_info=false;
    }
    else if (!account_info.contains(event.target)) {
        account_info.style.display = "none";
    }
})
account_info.style.display = "none"



function search() {
    if (search_input.value) {
        window.location.href = search_url + "?q=" + (search_input.value);
    }
}