'use strict';

document.getElementById("form").onsubmit = function(event) {
    //これが入るとページの再読み込みがなくなる
    //もし無いと・・・ボタン押すと、「#」のつくURLに変わる
    //　→　ブラウザが再読み込み  → #は何もないので初期画面表示　　となってしまう
    event.preventDefault();
    //
    const search = document.getElementById('form').word.value;
    console.log(search)
    document.getElementById('output').textContent = `[${search}]の検索中・・・`;
}

