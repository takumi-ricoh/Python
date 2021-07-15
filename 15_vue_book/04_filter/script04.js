'use strict';

//フィルタ登録
// Vue.filter('number_format', function(val){
//     return val.toLocaleString();
// })

//アプリ
let app = new Vue({
    el:'#app',
    data: {
        price:1000,
    },
    filters:{
        number_format: function(val){
            return val.toLocaleString();
        }
    }
})