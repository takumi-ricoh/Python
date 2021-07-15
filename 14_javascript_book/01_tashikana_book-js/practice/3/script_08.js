'use strict';

function fizzbuzz(n1,n2,num){
    if (num%n1===0 && num%n2===0){
        return  'fizzbuzz';
    }
    else if(num%n1===0){
        return 'fizz';
    }
    else if(num%n2===0){
        return 'buzz';
    }
    else{
        return num;
    }
}

for (let i=0; i<30; i++){
    let n1 = 3;
    let n2 = 5;
    let result = fizzbuzz(n1,n2,i);
    console.log(result);
}