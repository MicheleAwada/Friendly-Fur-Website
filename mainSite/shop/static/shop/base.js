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

