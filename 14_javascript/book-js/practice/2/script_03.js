'use strict';

// index_01.htmlの中の、id='choice'の要素を取得
// documentオブジェクトはHTMLやCSSを操作する機能がある
console.log(document.getElementById('choice'));


// textContentはプロパティの一つでコンテンツを表す
document.getElementById('choice').textContent = new Date();

// 文字列もOK
// document.getElementById('choice').textContent = '通知を受け取りますか?';

// 値なのでlog表示できる
console.log(document.getElementById('choice').textcontent);
