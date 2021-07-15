'use strict';

//pythonでいう辞書型
let jsbook = {title:'mybook',price:2500,stock:13}

//オブジェクトの扱い
console.log(jsbook.title);

//pythonの辞書っぽいアクセスもできる
console.log(jsbook['price']);

//値を変えてみる
jsbook.price = 5000;
console.log(jsbook.price);

//実はjavascriptではメソッドも格納してオブジェクトとよぶ
let object = {
    //メソッド
    addTax: function(a,b){
        return a+b;
    }
}
console.log(object.addTax(3,5));

//オブジェクトを読み取る時のforは、リストのときと違い、inを使う
//ただし順番は決まってない
console.log('jsbook',jsbook);
for(let p in jsbook){
    console.log('p=',p,'jsbook[p]=',jsbook[p]);
    //テンプレート文字列にして、HTMLに出してみる
    document.getElementById('list').insertAdjacentHTML('beforeend',`<li>${jsbook[p]}</li>`)
}

//リストでやるとどうなるか
jsbook=['a','b','c']
console.log('jsbook_list',jsbook);
for(let p in jsbook){
    console.log('p=',p,'jsbook[p]=',jsbook[p]);
}