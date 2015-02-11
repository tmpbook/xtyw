// JavaScript Document
$(document).keypress(function(event){
  if(event.which === 109){
    $('.dropdown').toggleClass('open');
  };
})
// 当点击M键的时候，class增加一个"open"
$(document).ready(pressm);
