'use strict';

const agree = Cookies.get('cookie-agree');
const panel = document.getElementById('privacy-panel');

if(agree==='yes'){
    console.log('クッキーを確認しました');
    document.body.removeChild(panel);
}else{
    console.log('クッキーを確認できません');
    document.getElementById('agreebtn').onclick = function(){
        Cookies.set('cookie-agree', 'yes', {expires:7});
        document.body.removeChild(panel);
    }
}

document.getElementById('testbtn').onclick = function(){
    Cookies.remove('cookie-agree');
}