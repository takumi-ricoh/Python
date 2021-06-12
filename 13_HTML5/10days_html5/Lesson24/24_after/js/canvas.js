// ページの読み込みが完了したら処理をする
window.addEventListener("load", function(){
	var ele = document.getElementById("status");
	// Canvasが使えるか調べる
	if (!window.HTMLCanvasElement){
		ele.innerHTML = "Canvasが使用できません";
		return;
	}
	// Canvasの要素
	var canvasObj = document.getElementById("myCanvas");
	// 2Dコンテキストの取得
	var context = canvasObj.getContext("2d");
	if (!context){
		ele.innerHTML = "2Dコンテキストが取得できません";
		return;
	}

	// 四角形を描画する
	context.fillStyle = "black";
	context.fillRect(0,0, canvasObj.width, canvasObj.height);
	context.strokeStyle = "rgba(255, 0, 0, 0.5)";
	context.lineWidth = 10;
	context.strokeRect(10,250, 200, 100);
	// 直線を描画する
	context.strokeStyle = "hsla(120, 100%, 50%, 0.5)";
	context.beginPath();
	context.moveTo(10,20);
	context.lineTo(250,350);
	context.stroke();
	// 円弧を描画する
	context.beginPath();
	context.strokeStyle = "orange";
	context.arc(90, 100, 50, 0, Math.PI, true);
	context.stroke();
	// 3次ベジエ曲線を描画する
	context.strokeStyle = "white";
	context.lineCap = "round";
	context.beginPath();
	context.moveTo(470, 50);
	context.bezierCurveTo(520, 120, 630, 100, 570, 260);
	context.stroke();
	// 三角形を描画する
	context.strokeStyle = "cyan";
	context.fillStyle = "blue"
	context.beginPath();
	context.moveTo(250, 30);
	context.lineTo(300, 150);
	context.lineTo(200, 150);
	context.closePath();
	context.fill();
	context.stroke();
	// クリッピング領域内に四角形を描画する
	context.save();
	context.beginPath();
	context.arc(430, 250, 90, 0, Math.PI*2, false);
	context.clip();
	context.strokeStyle = "yellow";
	context.lineWidth = 20;
	context.strokeRect(310,200, 200, 100);
	context.restore();
}, true);








