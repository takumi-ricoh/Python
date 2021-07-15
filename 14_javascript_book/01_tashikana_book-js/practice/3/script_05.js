'use strict';

//Dateクラスを使って、時間入手
const hour=new Date().getHours();

//かつ
if(hour >= 19 && hour < 21){
    window.alert('お弁当30%off');
}
//または
else if(hour==9 || hour==15){
    window.alert('お弁当1こおまけ');
}
else{
    window.alert('お弁当はいかが')
}