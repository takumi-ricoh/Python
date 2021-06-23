//1. elオプション
//HTMLとの紐付け
const app = new Vue({
    el: '#app'
})

//2. dataオプション
//データの登録
const app1 = new Vue({
    el: '#app-1',
    data: {
        name: '山田太郎'
    }
})

//3. methodsオプション
//関数定義
const app2 = new Vue({
    el: '#app-2',
    data: {
        items:['大吉','中吉','小吉','吉','凶','大凶'],
        fortune: 'ここに表示されるよ'
    },
    methods: {
        submit: function(){
            const items = this.items
            let item = items[Math.floor(Math.random() * items.length)]
            this.fortune = item
        }
    }
})

//4. computedオプション
//変更が無い場合、キャッシュされた値が使われる
const app3 = new Vue({
    el: '#app-3',
    data: {
        name : '',
        greeting: '',
        honorific: '',
        greetings: ['おはよう','こんにちは','こんばんは', 'おやすみ'],
        honorifics: ['さん', 'くん', 'ちゃん', '様', '殿']
    }, 
    computed: {
        message: function(){
            return this.greeting + ' ' + this.name + ' ' + this.honorific
        }
    }
})


//5.  watchオプション
const app4 = new Vue({
    el: '#app-4',
    data: {
        text: '初期値'
    },
    watch: {
        text: function(nextText, prevText){
            let prev = prevText;
            let next = nextText;
            if(!prev) prev = '未入力'
            if(!next) next = '未入力'
            alert('値が変更されました　前：' + prev + '→ 次：' + next)
        }
    }
})