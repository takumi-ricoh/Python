'use strict';

const number = Math.floor(Math.random() *6);
//parseInt：文字列を整数に変換する
const answer = parseInt(window.prompt('数あてゲーム。0～5の値を入力してね'));

let message;
if(answer===number){
    message='あたり';
}
else if(answer<number){
    message='残念でした。もっと大きい';
}
else if(answer>number){
    message='残念でした。もっと小さい';
}
else{
    message='0~5の値を入力してね';
}
window.alert(message);
