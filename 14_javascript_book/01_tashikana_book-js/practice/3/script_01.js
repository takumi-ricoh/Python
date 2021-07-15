'use strict';

/* 
window.confirmメソッドは、OK or キャンセル画面を表示
OKを押すとtrue、キャンセルだとfalseが、戻り値
*/
// console.log(window.confirm('ゲームスタート。準備はいい？'));

let res_of_confirm = window.confirm('準備はいい?')
if (res_of_confirm){
    document.getElementById('game_start').textContent='ゲーム開始！';
} 
else {
    document.getElementById('game_start').textContent='ゲーム開始しない!'
};
