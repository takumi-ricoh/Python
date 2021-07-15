'use strict';

//Vueクラスに渡せるオブジェクトは決まっている
let my_vue_ball = new Vue({
    el: '#vue_ball',
    // こう書いてもOK
    // el:  document.querySelector('#vue_ball'),
    data:{
        //コンポーネントが保持するデータ
        pos: {x:0, y:0},
        radius: 50,
    },
    methods:{
        //コンポーネントが持つメソッド
        move: function(x,y){
            this.pos.x += x;
            this.pos.y += y;
        }
    },
    filters:{
        //コンポーネントが持つフィルタ
    },
    computed:{
        //コンポーネントが持つ算出プロパティ
    },
    watch:{
        //コンポーネントが持つウォッチャ
    }
})

my_vue_ball.move(100,250);
my_vue_ball.radius = 40;