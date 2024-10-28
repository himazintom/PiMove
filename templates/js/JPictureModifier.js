window.onload = function() {
    updateSliderValue("sliderFrameVol", "sliderValueFrameVol");
};

function updateSliderValue(sliderId, sliderValueId) {
    //console.log("updateSliderValue");
    //console.log("sliderId: ",sliderId,"  sliderValueId: ",sliderValueId)
    var slider = document.getElementById(sliderId);
    //console.log("slider: ",slider)
    var sliderValue = document.getElementById(sliderValueId);
    sliderValue.textContent = slider.value;
}

function photoPreview(event) {//画像読み込みがbuttonから発生したときに呼び出される
    var fileInput = document.getElementById("fileInput");//ファイル選択ボタン取得
    var file = fileInput.files[0];//その中にあるファイルを取得
    var reader = new FileReader();//ファイルのリーダーをインスタンス化
    var startTime = Date.now();
    
    reader.onload = function(event) {
        console.log("htmlから画像を受け取りました")
        
        var img = document.createElement("img");
        img.setAttribute("id", "previewImage");
        img.setAttribute("src", "");
        img.setAttribute("loop", "true");
        var imageData = event.target.result
        var previewArea = document.getElementById("previewArea");
        previewArea.innerHTML = '';
        previewArea.appendChild(img);
        console.log("ajaxへリクエスト送信");
        console.log("受け取りから送信まで: " + (Date.now()-startTime) + "ミリ秒");
        
        // Ajaxリクエストを作成
        $.ajax({
            url: '/deform',
            type: 'POST',
            data: { image_data: imageData },
            success: function(response) {
                img.src=response
                console.log('画像のアップロードに成功しました:', response);
            },
            error: function(error) {
                console.error('画像のアップロード中にエラーが発生しました:', error);
            }
        });
    };
    reader.readAsDataURL(file);
    console.log("pythonへ画像を送ってから表示までかかった時間: " + (Date.now()-startTime) + "ミリ秒");
}