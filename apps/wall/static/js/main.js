function rewriteDocument(html) {
  newDoc = document.open("text/html", "replace")
  newDoc.write(html)
  newDoc.close();
}
//
// function formSubmit(event, successFunc=null) {
//   event.preventDefault(); // avoid to execute the actual submit of the form.
//   var url = this.url; // the script where you handle the form input.
//
//   $.ajax({
//     type: "POST",
//     url: url,
//     data: this.serialize(), // serializes the form's elements.
//     success: function(data) {
//       rewriteDocument(response);
//       if (successFunc) {
//         successFunc();
//       }
//     }
//   });
// }
//
// function initAjaxRequests() {
//
//   $('a').click(function (event){
//      event.preventDefault();
//      $.ajax({
//         url: $(this).attr('href'),
//         success: rewriteDocument(response)
//      })
//   });
//
//   $('form').submit(formSubmit(event));
//
//   console.log($('#login_form'));
//   $('#login_form').submit(function(event) {
//     formSubmit(event, successFunc=function(){
//       console.log(data);
//       // localStorage.setItem('jwt', )
//     })
//   });
// }
//
//


function initAjaxRequests() {

    $.ajaxSetup({
        headers: { 'jwt': localStorage.getItem('jwt') }
    });

    $('a').click(function (event){
       event.preventDefault();
       $.ajax({
          url: $(this).attr('href'),
          success: function(data) {
            rewriteDocument(data);
          }
       })
    });
}

$(document).ready(initAjaxRequests());
