window.onload = function() {

    // let form_calendars =  document.querySelectorAll('.form_calendar');
    //
    // for(form_calendar of form_calendars){
    //     form_calendar.addEventListener('click', function (){
    //        let input = this.previousElementSibling;
    //        console.log(input)
    //         input.setAttribute('type', 'date')
    //     });
    // }

  let input_dates =  document.querySelectorAll('.input_date');

    for(input_date of input_dates){
        input_date.setAttribute('type', 'date')
        }

    /*=== получене куки для переключателя объектов ===*/

    if ($.cookie("object") == null) {
      $.cookie("object", "1");
      $("#object-1").attr("checked", "checked");
    }
    else {
      $('#object-' + $.cookie("object")).attr("checked", "checked");
    };
    /*===  end получене куки для переключателя объектов ===*/

}

function chang_object(){
  let object = $(".switch_object input:checked").val();
  jQuery.cookie("object", object);
  // window.location.reload();
  window.location.href = path;
};