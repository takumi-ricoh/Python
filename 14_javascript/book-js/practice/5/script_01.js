'use strict';

function countdown(due){
    const now = new Date();
    //getTime()はUnixタイムをミリ秒で返す
    const rest = due.getTime() - now.getTime();

    const sec = Math.floor(rest / 1000) % 60;
    const min = Math.floor(rest / 1000 / 60) % 60;
    const hours = Math.floor(rest / 1000 / 60 / 60) % 60;
    const days = Math.floor(rest / 1000 / 60 / 60 / 24);
    
    const count = [days, hours, min, sec];

    return count;
}

/* =======================時刻のカウントダウン=========================*/

//終了時間の設定
let goal = new Date();
goal.setHours(23);
goal.setMinutes(59);
goal.setSeconds(59);
console.log(countdown(goal))

function recalc(){
    const counter = countdown(goal);
    const timer = `${counter[1]}時間${counter[2]}分${counter[3]}秒`
    document.getElementById('timer').textContent = timer
    refresh();
}

function refresh(){
    //1秒後にまたrecalcをコールバックする
    setTimeout(recalc, 1000);
}

//初回のrecalc実行
recalc();


/* =======================大阪万博のカウントダウン=========================*/
let goal2 = new Date(2025,4,3);

function recalc2(){
    const counter = countdown(goal2);
    const timer = `${counter[0]}日${counter[1]}時間${counter[2]}分${counter[3]}秒`
    document.getElementById('day').textContent = counter[0]
    document.getElementById('hour').textContent = counter[1]
    document.getElementById('min').textContent = String(counter[2]).padStart(2,'0')
    document.getElementById('sec').textContent = String(counter[3]).padStart(2, '0')   
    refresh2();
}

function refresh2(){
    //1秒後にまたrecalcをコールバックする
    setTimeout(recalc2, 1000);
}

//初回のrecalc実行
recalc2();