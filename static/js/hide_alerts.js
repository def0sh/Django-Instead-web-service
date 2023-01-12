// login alert hide
const close_mes = function () {
    $("#alert-error").fadeOut();
}
$("#btn-close").on("click",close_mes);
setTimeout(close_mes,3500)


// info messages alerts hide
$('.alert').delay(2000).fadeOut();
