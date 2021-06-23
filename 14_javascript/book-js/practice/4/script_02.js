'use strict';

//オブジェクト生成
const now = new Date();
//メソッド使う
const year = now.getFullYear();
const month = now.getMonth()
const date = now.getDate();
const hour = now.getHours();
const min = now.getMinutes();



//-----ただの表示
document.getElementById('time_def').textContent = `${now}`;

//----ちゃんと書き換えたもの
//月はなぜか-1されたものが返るので1足してる
const output = `${year}/${month + 1}/${date} ${hour}:${min}`;
document.getElementById('time').textContent = output;

//------さらにAMPM加えたもの
//午前午後に変換
let ampm = '';
if(hour <  12){
    ampm = 'a.m';
}
else{
    ampm = 'p.m';
}
//output
const output_ampm = `${year}/${month + 1}/${date} ${hour % 12}:${min}${ampm}`;
document.getElementById('time_ampm').textContent = output_ampm;