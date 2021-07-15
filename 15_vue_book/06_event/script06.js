'use strict';

let app = new Vue({
    el: '#app',
    data: {
        stock:10
    },
    methods: {
        //削除ボタンのクリックイベントハンドラ
        onDeleteItem: function(){
            this.stock -= 1
        },
        onAddItem: function(){
            this.stock += 1
        }
    }

})