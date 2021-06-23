// 1. v-bind
const app1 = new Vue({
    el: '#app-1',
    data: {
        url: 'https://www.google.com/'
    }
})


// 2. v-model
const app2 = new Vue({
    el: '#app-2',
    data: {
        inputText:'初期値'
    }
})

// 3. v-on
const app3 = new Vue({
    el: '#app-3',
    data: {
        count:0
    },
    methods: {
        counter: function(){
            this.count++
        },
        counter2: function(){
            this.count=0
        }
    }
})

//4. v-if
const app4 = new Vue({
    el: '#app-4',
    data: {
        isMember: true,
        isPremier: false,
    }
})

//5. v-show
const app5 = new Vue({
    el: '#app-5',
    data: {
        isVisible: true
    }
})

//6. v-for
const app6 = new Vue({
    el: '#app-6',
    data: {
        foods: [
            { id: 1, name: 'ハンバーグ'},
            { id: 2, name: '焼き肉'},
            { id: 3, name: 'ステーキ'},
            { id: 4, name: 'すき焼き'},
        ]
    }
})

//7. v-once
const app7 = new Vue({
    el: '#app-7',
    data: {
        count:0
    }, 
    methods: {
        counter: function(){
            this.count++
        }
    }
})