'use strict';

let x = new Vue({
    el: "#app",
    data:{
        message: 'まだある',
        stock: 10,
    }, 
    //値を小さくする
    methods:{
        onDeleteItem: function(){
            this.stock -= 1;
        }
    },

    //ウォッチャを使うパタン
    watch: {
        stock: function(newstock,oldstock){
            if (newstock==0){
                this.message = '売り切れ'
            }
        }
    },

    //算出プロパティを使うパターン
    computed: {
        statusmessage: function(){
            if (this.stock == 0){
                return '売り切れ'
            }
            return 'まだある'
        }
    }
});