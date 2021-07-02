'use strict';
$(document).ready(function() {
    //基本形
    $.ajax({url: 'data.json', dataType: 'json'})

    //データがダウンロードできたときの処理
    .done(function(data){
        data.forEach(function(item,index){
            if(item.crowded === 'yes'){
                const idName = '#' + item.id;
                $(idName).find('.check').addClass('crowded')
            }
            console.log(item)
        })
    })
    //データがダウンロードできなかったときの処理
    .fail(function(){
        window.alert('読み込みエラー')
    });

    //クリックされたら空き席状況を表示
    $('.check').on('click', function(){
        if($(this).hasClass('crowded')){
            $(this).text('残席わずか').addClass('red');
        } else {
            $(this).text('お席あります').addClass('green');
        }
    })
});