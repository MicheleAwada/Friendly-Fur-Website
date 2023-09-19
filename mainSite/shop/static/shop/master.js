function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

function updateTextColorBasedOnBackground(elementId) {
  // Get the selected element by its ID
  const element = document.getElementById(elementId);

  if (element) {
    // Get the background color as a string (e.g., "rgb(255, 255, 255)")
    const bgColor = window.getComputedStyle(element).backgroundColor;

    // Calculate the brightness of the background color
    // You can use different formulas for calculating brightness; here's one approach:
    const brightness =
      (parseInt(bgColor.slice(4, -1).split(', ').reduce((acc, val) => acc + parseInt(val), 0)) / 3) / 255;

    // Determine the text color based on the background brightness
    const textColor = brightness > 0.6 ? 'black' : 'white';

    // Set the text color
    element.style.color = textColor;
  }
}


$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})