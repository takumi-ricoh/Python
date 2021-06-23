'use strict';

//1.(リストレンダリング)
const vm1 = new Vue({
    el: '#example1',
    data: {

        items: [
            {
                name: 'みかん',
                price: '100'
            }, 
            {
                name: 'もも',
                price: '300'
            }, 
            {
                name: 'いちじく',
                price: '500'
            }, 
        ],

    },
    computed: {
        priceWithTax: function(){
            let result = [];
            for (let item of this.items){
                result.push(item.price*1.08)
            }
            return result;
        }, 
    }
});

//2.条件付きレンダリング
const vm2 = new Vue({
    el: '#example2',
    data: {
        name: '',
    },
    computed: {
        isValid: function(){
            return this.name.length > 5;
        }
    }
});

//3.イベント
const vm3 = new Vue({
    el: "#example3",
    data: {
        name1:'',
        name2:'',
        name3:'',
        name4:'',
        temp:'',
    },
    methods:{
        //エンターで書き換える
        updateName: function(event){
            this.name2 = event.target.value
        },
        //ボタンクリックで動く
        showData: function(){
            this.name4 = this.temp
        }

    }
})

//4.v-model
const vm4 = new Vue({
    el: "#example4",
    data: {
        name:'',
    }
})