'use strict';

// constは「定数」　値の変更不可
const answer2 = window.prompt('ヘルプをみますか？(const)');

if(answer2==='yes'){
    window.alert('タップでジャンプ、障害物を避けます');
}
else if(answer2==='no'){
    window.alert('ゲーム起動中');
}
else{
    window.alert('yesかnoかでお答えください');
}