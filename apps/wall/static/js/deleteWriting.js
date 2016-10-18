$(".delete_writing_button").click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
        url: '/' + '?' + $.param({
          "writing_key": $(this).children(":first").attr('value')
        }),
        type: 'DELETE',
        success: function(result) {
            window.location.href = '/';
        }
    });
});
