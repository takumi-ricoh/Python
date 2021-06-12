// ワーカーにCanvasの情報を渡す
window.addEventListener("load", function(){
	var ele = document.getElementById("result");
	// Web Workersが使えるか調べる
	if (!window.Worker){
		ele.innerHTML = "Web Workersは使用できません";
		return;
	}
	// Canvasの情報を読み出す
	var canvasObj = document.getElementById("myCanvas");
	var w = canvasObj.width;
	var h = canvasObj.height;
	var context = canvasObj.getContext("2d");

	// ボタンがクリックされた時の処理
	document.getElementById("calc").addEventListener("click", function(){
		// 調べる輝度の値を読み出す
		var R = document.getElementById("red").value;
		var G = document.getElementById("green").value;
		var B = document.getElementById("blue").value;
		// ピクセルデータを読み出す
		var image = context.getImageData(0, 0, w, h);
		// data配列にピクセルデータが格納されている
// ---- 初版からの変更箇所ここから
		// var pixels = image.data;
		for(var p=0, pixels=[ ]; p<image.data.length; p++){ pixels[p] = image.data[p]; }
// ---- 初版からの変更箇所ここまで
		var myWorker = new Worker("js/calcPixel.js");
		myWorker.onmessage = function(evt){
			ele.innerHTML = "ピクセル数："+evt.data;
		}
		ele.innerHTML = "ピクセル数を計算中...";
		myWorker.postMessage({
			width: w,
			height: h,
			pixelData : pixels,
			red : R,
			green : G,
			blue : B
		});
	}, true);
	// ヒストグラムを表示ボタンがクリックされた時の処理
	document.getElementById("histgram").addEventListener("click", function(){
		// ピクセルデータを読み出す
		var image = context.getImageData(0, 0, w, h);
		// data配列にピクセルデータが格納されている
// ---- 初版からの変更箇所ここから
		// var pixels = image.data;
		for(var p=0, pixels=[ ]; p<image.data.length; p++){ pixels[p] = image.data[p]; }
// ---- 初版からの変更箇所ここまで
		var myWorker = new Worker("js/histgram.js");
		myWorker.onmessage = function(evt){
			ele.innerHTML = "";
			var maxPixel = w  * h;	// ピクセルの総数
			var histgram = evt.data;	// ワーカーで計算した結果
			for(var i=0; i<256; i++){
				var bar = document.createElement("div");
				var n = (histgram[i] / maxPixel) * 10000;	// 横幅を計算
				bar.style.width = n +"px";
				bar.className = "pixelbar";
				ele.appendChild(bar);
			}
		}
		ele.innerHTML = "ヒストグラムの処理中...";
		myWorker.postMessage({
			width: w,
			height: h,
			pixelData : pixels
		});
	}, true);
	// Canvasに画像を描画する
	var imageObj = new Image();
	imageObj.src = "images/flower.jpg";
	imageObj.onload = function(){
		context.drawImage(imageObj, 0, 0, 320, 240);
	}
}, true);
