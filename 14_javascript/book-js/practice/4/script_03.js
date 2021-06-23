'use strict';

//円周率計算
const pi = Math.PI;

//そのまま表示
document.getElementById('pi').textContent = `${pi}`

//関数
function point(num,digit){
    const mover = 10 ** digit;
    return Math.floor(num*mover)/mover;
}

//切り捨て
document.getElementById('pi_int').textContent = `${point(pi,0)}`

//切り捨て
document.getElementById('pi_two').textContent = `${point(pi,2)}`