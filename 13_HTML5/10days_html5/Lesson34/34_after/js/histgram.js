// ヒストグラムを計算
onmessage = function(evt){
	var w = evt.data.width;
	var h = evt.data.height;
	var pixels = evt.data.pixelData;
	var histgramArray = [ ];
	for(var i=0; i<256; i++){
		histgramArray[i] = 0;
	}
	for(var y=0; y<h; y++){
		for(var x=0; x<w; x++){
			var pointer = (y * w + x ) * 4;	// RGBαなので4つの配列要素
			var red = pixels[pointer+0];	// 赤の輝度（0〜255）
			var green = pixels[pointer+1];	// 緑の輝度（0〜255）
			var blue = pixels[pointer+2];	// 青の輝度（0〜255）
			var g = Math.floor(green * 0.6 + red * 0.3 + blue * 0.1);
			histgramArray[g]++;	// 輝度を1つ増やす
		}
	}
	postMessage(histgramArray);
}
