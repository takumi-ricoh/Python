'use strict';

//geolocationがコールする関数(成功時)
function success(pos) { 
    ajaxRequest(pos.coords.latitude, pos.coords.longitude);

 }
//geolocationがコールする関数
 function fail(error){
    alert('位置情報の取得に失敗しました。エラーコード：' + error.code);
 }

 //現在位置の取得
 navigator.geolocation.getCurrentPosition(success,fail);

//変数に入れてみる
 let data_res;

//UTCをミリ秒に
function utcToJSTime(utcTime){
    return utcTime*1000;
}




// // 表示オブジェクト
// class ViewObj {
//     //コンストラクタ
//     constructor(data){
//         this.data = data;
//     }
//     //メソッド
//     data_pickup(){
//         this.data.list.forEach(function(forecast,index){
//             let dateTime = new Date(utcToJSTime(forecast.dt));
//             let month    = dateTime.getMonth()+10;	//
//             let date     = dateTime.getDate();
//             let hours    = dateTime.getHours();
//             let min      = String(dateTime.getMinutes()).padStart(2,'0');
//             let temperature = Math.round(forecast.main.temp);
//             let description = forecast.weather[0].description;
//             let iconPath    = `images/${forecast.weather[0].icon}.svg`

//             this.change_output(index);
//         }),
//         console.log("test")
//     }
    
//     //メソッド
//     //現在の天気とそれ以外で出力を変える
//     change_output(index){
//         if(index === 0){
//             const currentWeather = `
//             <div class="icon"><img src="${iconPath}"></div>
//             <div class="info">
//                 <p>
//                     <span class="description">現在の天気:${this.description}</span>
//                     <span class="temp">現在の気温:${this.temperature}</span>
//                 </p>
//             </div>`;
//             $('#wheather').html(currentWeather);
//         }
//         else{
//             const tableRow = `
//             <tr>
//                 <td class="info">
//                     ${month}/${date} ${hours}:${min}
//                 </td>
//                 <td class="icons"><img src="${iconPath}"></td>
//                 <td><span class="description">${description}</span></td>
//                 <td><span class="temp">${temperature}</span></td>
//             </tr>`;
//         }
//     }
// }

 //　天気データ取得
function ajaxRequest(lat, long){
     const url = 'https://api.openweathermap.org/data/2.5/forecast';
     const appId = '925e0910fe8842a76fd57cb46af662a1';

     $.ajax({
         url: url,
         data: {
             appId: appId,
             lat: lat,
             lon: long,
             units:'metric',
             lang: 'ja'
         }
     })
     .done(function(data){
         //おまけ
         console.log('$.ajax succeed !!')
         data_res=data;
         //クラスで実行：うまくいかない。。。
        //  let viewobj=new ViewObj(data);
        //  viewobj.data_pickup()

        //都市名・国名
        $('#place').text(data.city.name + ',' + data.city.country);

        data.list.forEach(function(forecast,index){
            const dateTime = new Date(utcToJSTime(forecast.dt));
            const month    = dateTime.getMonth()+10;	//
            const date     = dateTime.getDate();
            const hours    = dateTime.getHours();
            const min      = String(dateTime.getMinutes()).padStart(2,'0');
            const temperature = Math.round(forecast.main.temp);
            const description = forecast.weather[0].description;
            const iconPath    = `images/${forecast.weather[0].icon}.svg`

            if(index === 0){
                const currentWeather = `
                <div class="icon"><img src="${iconPath}"></div>
                <div class="info">
                    <p>
                        <span class="description">現在の天気:${description}</span>
                        <span class="temp">現在の気温:${temperature}</span>
                    </p>
                </div>`;
                $('#wheather').html(currentWeather);
            }
            else{
                const tableRow = `
                <tr>
                    <td class="info">
                        ${month}/${date} ${hours}:${min}
                    </td>
                    <td class="icons"><img src="${iconPath}"></td>
                    <td><span class="description">${description}</span></td>
                    <td><span class="temp">${temperature}</span></td>
                </tr>`;
            }
        });
     })
     .fail(function(){
         console.log('$.ajax failed');
     })
 }

 