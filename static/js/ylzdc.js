// 当点击M键的时候，class增加一个"open"
//$(document).keypress(function(event){
//  if(event.which === 109){
//    $('.dropdown').toggleClass('open');
//  };
//})

//$(document).keypress(function(event){
//  if(event.which === 110){
//    $('.left_space').toggle(50);
//    $('.right_space').toggle(50);
//    $('.middle_space').toggleClass('col-md-8');
//  };
//})
var main = function() {
    $('.article').click(function() {
        $('.article').removeClass('info');
        $('.article').children('.has_desc').children('.description').hide();
        $(this).addClass('info');
        $(this).children('.has_desc').children('.description').show();
    });
};

$(document).ready(main);
//$(document).ready(pressm);
