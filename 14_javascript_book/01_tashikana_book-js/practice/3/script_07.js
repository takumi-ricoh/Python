'use strict';

// pythonと似てる
function total(price){
    const tax = 0.1;
    return price + price * tax;
}

//結果
let base_price = 8000;
let result;
result = total(base_price);
console.log('税込み価格',result);


// 繰り返しでHTMLにアウトプット
let i=0;
while(i<3){
    let id = 'output' + (i+1).toString();
    let content = '税込み価格は' + total(i*100).toString();

    //textContentはイミュータブルなので、このように渡さないと書き換え不可
    //tmp = ~.textContent　→　tmp = 別の値　　みたいのはできない
    //javascriptのリストもpython同様ミュータブル
    document.getElementById(id).textContent = content;

    i+=1;
}