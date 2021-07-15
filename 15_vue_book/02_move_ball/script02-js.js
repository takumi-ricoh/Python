'use strict';

// =====オブジェクトとしての設計========
let ball = {
    pos:{
        x:10,
        y:50
    },
    move: function(x,y){
        this.pos.x += x;
        this.pos.y += y;
    }
}

//オブジェクト
console.log('======オブジェクト=====')
console.log(ball.pos.x);
console.log(ball.pos.y);
//位置変更
ball.move(10,20);
console.log(ball.pos.x);
console.log(ball.pos.y);


// =========動くものクラス==========
let Movable = function(x,y){
    this.pos = {
        x: x,
        y: y
    },
    this.move = function(x,y){
        this.x += this.x;
        this.y += this.y;
    }
}

//オブジェクト
console.log('======クラス=====')

//100個インスタンス化
let balls = []

for (let i=0;i<=100;i++){
    let x = Math.floor(Math.random()*window.innerWidth)
    let y = Math.floor(Math.random()*window.innerHeight)
    let movable_ball = new Movable(x,y);
    balls.push(movable_ball)
}

//ブラウザに表示する
balls.forEach(function(item,index){
    let tmp = '<div class="ball" style="top:' + item.pos.y + 'px; left:' + item.pos.x + 'px;">●</div>';
    document.write(tmp)
    })


