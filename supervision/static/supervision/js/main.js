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

}