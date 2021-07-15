
let app1 = new Vue({
    el: '#app1',
    data:{
        message: 'はひふえほ',

        message_ja: 'こんちは',
        message_en: 'hey',
        lang: 'ja'
    }
});

let app2 = new Vue({
    el: '#app2',
    data:{
        message: 'こんにちは！！',
        pSize: '40px',
        isCapital: false,
    }
})

let app3 = new Vue({
    el: '#app3',
    data: {
        products:[
            {code:123,name:"りんご"},
            {code:223,name:"なし"},
        ]
    }
})

let app4 = new Vue({
    el: '#app4',
    data: {
        price: 990
    }
})
