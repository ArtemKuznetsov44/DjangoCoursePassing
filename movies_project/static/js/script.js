// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//
// $(function($) {
//      $('#filter_form').on("submit", function(event) {
//         event.preventDefault();
//         console.log(this)
//
//         let data = $(this).serializeArray();
//         let info = {
//             'years': [],
//             'genres': []
//         }
//
//
//         data.forEach(function(element) {
//             if (element.name === "year") {
//                 info['years'].push(element.value)
//             }
//             else {
//                 info['genres'].push(element.value)
//             }
//         });
//
//
//         console.log(data);
//
//         $.ajax({
//             type: this.method,
//             url: this.action,
//             dataType: 'json',
//             data: info,
//             success: function(response) {
//                 console.log('ok - ', response);
//                 window.location.reload();
//             },
//             error: function(response) {
//                 console.log('error - ', response)
//             }
//         })
//     });
// })


// Event before window reloading:
window.addEventListener('beforeunload', function () {
    // scrollY - property which returns the scroll on Y value.
    // scrollTop - the same thing, but it works with elements on page.

    // Save in localStorage the value of scrollTop property (values in localStorage we can use after page reload):

    this.localStorage.setItem('scrollPosition', document.documentElement.scrollTop.toString())
})
// Event in time when page is loading:
window.addEventListener('load', function () {

    /** @type {number}*/
    // Getting item from localStorage:
    let scrollPosition = parseInt(this.localStorage.getItem('scrollPosition'));

    // If it is not null:
    if (scrollPosition !== null) {
        // Find interesting element and make scroll to (xPosition, yPosition).
        // yPosition is the value from localStorage.
        this.document.querySelector(".right-part").scrollTo(0, scrollPosition);
        this.localStorage.removeItem('scrollPosition')
    }
})
