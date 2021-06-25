'use strict';

const images = ['images/image1.jpg', 'images/image2.jpg', 'images/image3.jpg','images/image4.jpg','images/image5.jpg'];
let current = 0;

//画像のプリロード
images.forEach(function(item,index){
    preloadImage(item);
})

//画像のプリロード関数
function preloadImage(path){
    // createElementは、要素をつくる
    // 引数を'img'としたので<img></img>ができる
    // これはメモリ上の話なのでHTMLに書き込まれるわけではない
    let imgTag = document.createElement('img');
    imgTag.src = path;
}

//画像ソースを切り替える
function changeImage(num){
    if (current + num >=0 && current + num < images.length){
        current += num;
        document.getElementById('main_image').src = images[current];
        pageNum();
    }
}

//pageの<div>要素に文字列を挿入
function pageNum(){
    document.getElementById("page").textContent = `${current + 1} / ${images.length}`;
}


pageNum();

//prevの<div>要素がクリックされると,,,,,,,,
document.getElementById('prev').onclick = function(){
    changeImage(-1)
}

document.getElementById('next').onclick = function(){
    changeImage(1)
}
