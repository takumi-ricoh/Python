'use strict';

let app = new Vue({
    el: '#app',
    data: {
        year: (new Date()).getFullYear()
    },
    computed: {
        isUrudoshi: function(){
            console.log('kita')
            if ((this.year % 4 === 0) && (this.year % 100 != 0) || (this.year % 400 === 0)){
                    return true
                }
            else{
                return false
            }
        }
    }
})