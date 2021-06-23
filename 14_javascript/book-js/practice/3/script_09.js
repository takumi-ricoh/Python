'use strict';

let todo = ['a','b','c','d','e'];
// pythonのappendが、push
todo.push('aaaa');


function add_str(){
    return '今の値は：'
}


//埋め込み! 
//親要素<ul>の後ろから詰めて挿入
document.getElementById('list').insertAdjacentHTML('beforeend','<h1>やってみた</h1>')


// for (item of ~) で　,pythonの for item in ~ と同じ 
for(let item of todo){

    //テンプレート文字列作成は、バックスティック「`」で囲む
    //中に${}とすると変数を埋め込める
    const li = `<li>${add_str()} ${item} ${3+5}</li>`;
    
    //HTMLに埋め込み！
    //親要素<ul>に、子要素<li>をうめこんだ
    document.getElementById('list').insertAdjacentHTML('beforeend',li);
}