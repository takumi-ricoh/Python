'use strict';

let i=1;
while(i<=10){
    //文字と整数を足せてしまう!?
    console.log(i + '枚')
    // i=i+1;
    i+=1;

}

let enemy=100;
let count=0;
window.alert('戦闘スタート');
while(enemy>0){
    const attack = Math.floor(Math.random()*30)+1;
    //これでも行ける。
    console.log('モンスターに',attack,'のダメージ');
    enemy -= attack;
    count += 1;
}

//NG：スコープ外
//console.log(attack);

console.log(count,'回でモンスターを倒した');

// 無限ループ
// while(true){
//     console.log('abc');
// }