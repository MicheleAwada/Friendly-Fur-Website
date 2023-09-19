var fail = document.getElementById("fail");
var check = document.getElementById("check");
var load = document.getElementById("load");
var error = document.getElementById("error");
function invisible(result) {
        if (result !== -1) {
            load.classList.remove("visible");
            load.classList.add("invisible");
        } else {
            load.classList.remove("invisible");
            load.classList.add("visible");
        }

        if (result !== 0) {
            check.classList.remove("visible");
            check.classList.add("invisible");
        } else {
            check.classList.remove("invisible");
            check.classList.add("visible");
        }

        if (result !== 1) {
            fail.classList.remove("visible");
            fail.classList.add("invisible");
        } else {
            fail.classList.remove("invisible");
            fail.classList.add("visible");
        }

        if (result !== 2) {
            error.classList.remove("visible");
            error.classList.add("invisible");
        } else {
            error.classList.remove("invisible");
            error.classList.add("visible");
        }
}

var email = document.getElementById("id_email");
function ValidateEmail(mail) 
{
if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
{
    return (true)
}
    return (false)
}
let timeoutId;
function valid_email () {
    clearTimeout(timeoutId);
    var emailval = email.value;
    invisible(-1);
    if (!emailval) {
        return invisible(3);
    }
    if (ValidateEmail(emailval)) {
        timeoutId = setTimeout(() => {
        console.log('Function executed after 2 seconds of no input.');
        return valid_email_ajax();
        },
        1000);
        return;

        
    }
    return invisible(2);

    
}
function valid_email_ajax() {
    var emailval = email.value;
    invisible(-1);
    $.ajax({
    url: ajax_url,
    type: "POST",
    dataType: "json",
    data: JSON.stringify({email: emailval,}),
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
        var result = data['is_email_valid'];
        invisible(result);
    },
    error: (error) => {
        console.log(error);
    }
    });
}
email.addEventListener("input", (event) => {
    valid_email();
});
valid_email();