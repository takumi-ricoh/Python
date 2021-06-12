window.addEventListener("load", function(){
	// a要素を読み出し
	var tSwitch = document.getElementById("toggleSwitch");
	// a要素にイベントを割り当て
	tSwitch.addEventListener("click", function(){
		var tbl = document.querySelectorAll("table");
		if (tbl[0].style.display == "none"){
			tbl[0].style.display = "block";
			tSwitch.innerHTML  = "▲売上表を表示しない";
		}else{
			tbl[0].style.display = "none";
			tSwitch.innerHTML  = "▲売上表を表示する";
		}
	}, true);
	// バナー広告を定期的に入れ替え
	setInterval(function(){
		// 広告設定
		var cm = [ ];
		cm["images/banner.png"] = "images/banner2.png";
		cm["images/banner2.png"] = "images/banner.png";
		// img要素を読み出し
		var img = document.querySelectorAll("aside img")[0];
		// 属性値を入れ替え
		img.src = cm[img.getAttribute('src')];
	}, 1000);
	// 現在の日時をセクションの最後に追加する
	var dtObj = new Date();	// Dateオブジェクトを作成
	var y = dtObj.getFullYear();	// 西暦年数4桁を読み出し
	var m = dtObj.getMonth() + 1;	// 月を読み出し
	var d = dtObj.getDate();	// 日にちを読み出し
	document.querySelectorAll("time")[0].innerHTML = y+"/"+m+"/"+d;
	// 新たなバナーを追加する
	var bannerImage = new Image();	// 画像オブジェクトを作成
	bannerImage.src = "images/banner3.png";	// URLを指定
	bannerImage.onload = function(){
		var aDiv = document.querySelectorAll("aside div")[0];
		aDiv.appendChild(bannerImage);
	}
	// 売り上げがマイナスの場合は赤文字にする
	var td = document.querySelectorAll("#main table td");
	for(var i=0; i<td.length; i++){
		var text = td[i].innerHTML;
		if (text.indexOf("-") > -1){
			td[i].style.color = "red";
		}
	}
}, true);
