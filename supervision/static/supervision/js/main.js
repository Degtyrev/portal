window.onload = function() {
// let input_date = document.querySelector('.input_date')
//     input_date.onclick = function(){
//         console.log('gdtrtrgdg')
//     }

document.getElementById('id_start').onchange = function(){changeDate()}

function changeDate(){
    var x =document.getElementById('id_start')
    let condition = document.getElementById('id_status')
    let val = x.value
    let a = Date.parse(val)
   console.log(a)
   console.log(condition)


    let now = Date.now();
    console.log(now)
    if (now < a) {
        condition.value =2
    }

}


};