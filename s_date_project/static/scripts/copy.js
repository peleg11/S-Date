$(document).on('click', '.copy', function(e){
    e.preventDefault(); //for <a>
    $('.paste').val($(this).text());
});
