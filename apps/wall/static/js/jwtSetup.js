if (localStorage.getItem('jwt')) {
  $.ajaxSetup({
      headers: { 'jwt': localStorage.getItem('jwt') }
  });
  // $.ajax({
  //   url: '/',
  //   success: rewriteDocument(response)
  // });

  $(document).ready(initAjaxRequests());

}

$('#login_form').submit(function(event) {
    event.preventDefault(); // avoid to execute the actual submit of the form.
    var url = this.action; // the script where you handle the form input.

    $.ajax({
      type: "POST",
      url: url,
      data: $('#login_form').serialize(), // serializes the form's elements.

      success: function(data, textStatus, request) {
        localStorage.setItem('jwt', request.getResponseHeader('jwt'));
        $.ajax({url: '/', success: rewriteDocument(data)});
      }
    });

});
