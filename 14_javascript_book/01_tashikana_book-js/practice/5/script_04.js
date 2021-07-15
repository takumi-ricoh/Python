'use strict';

//thumbがつくクラスの要素を配列として全部取得
const thumbs = document.querySelectorAll('.thumb');

//for
thumbs.forEach(function(item,index){
    item.onclick = function(){
        //data-iamge　→ dataset.image として取得
        console.log(this.dataset.image)
        //クリックした画像が大きくなる
        document.getElementById('bigimg').src = this.dataset.image;
    }
})