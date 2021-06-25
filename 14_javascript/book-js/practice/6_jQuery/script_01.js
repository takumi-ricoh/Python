'use strict';

$(document).ready(function(){
    $('.submenu h3').on('click',function(){
        $(this).next().toggleClass('hidden');
    });
});

$(document).ready(function(){
    $('.submenu h3').hover(function(){
        $(this).next().toggleClass('hidden');
    });
});