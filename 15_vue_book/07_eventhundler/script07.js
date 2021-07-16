'use strict';

let x = new Vue({
    el: '#app',
    data:{
        point:{x:0,y:0}
    },
    //インスタンス生成時に特別に実行される
    created: function(){ 
        //この下にさらに複数処理を切れることもできる
        
        //マウスが動いたら、mousemoveHandolerをコール
        addEventListener('mousemove',this.mousemoveHandler)
    },

    //インスタンス破棄の直前
    beforeDestroy: function(){

        addEventListener('mousemove',this.mousemoveHandler)
    },

    methods:{
        //コールバックされる関数
        mousemoveHandler: function($event){
            this.point.x = $event.clientX;
            this.point.y = $event.clientY;
        }
    },
})