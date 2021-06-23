/************   1.コンポーネント ******************/

//子コンポーネント
const fruitsListChild = Vue.extend({
    template: '<p>子コンポーネント</p>'
  })
  
//親コンポーネント
const fruitsListParent = Vue.extend({
    template: '<div>親コンポーネント<fruits-list-child></fruits-list-child></div>',
    components: {
    'fruits-list-child': fruitsListChild
    }
})

//親コンポーネントをインスタンス化
new Vue({
    el: "#fruits-list",
    components: {
        'fruits-list-parent': fruitsListParent
    }
})

/************   2.コンポーネント ******************/

//子コンポーネント
Vue.component('fruits-list', {
    props: ['fruitsItem'],
    template: '<li>{{fruitsItem.name}}</li>'
  });


new Vue({
    el: '#fruits-component',
    data: {
        fruitsItems: [
        {name: '梨'},
        {name: 'イチゴ'}
        ]
    }
});