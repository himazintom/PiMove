// ゲームパッドのスティック要素
const stick = document.getElementById("stick");
const stickContainer = document.querySelector(".stick-container");
// ゲームパッドのスティックの現在位置
let stickX = 0;
let stickY = 0;

// ゲームパッドのスティックの最大移動距離
let maxDistance=75

// ゲームパッドのスティックのリセットイベント
function handleStickReset() {
  stickContainer.removeEventListener("mousemove", handleStickMove);
  // スティックの位置をリセット
  stickX = 0;
  stickY = 0;

  // スティックの要素を中央に移動
  stick.style.transform = "translate(-50%, -50%)";

  // x軸とy軸の値を表示
  console.log("x軸:", stickX.toFixed(2), "y軸:", stickY.toFixed(2));
}
function handleStickStart(){
    if(checkDevice()){
        stickContainer.addEventListener("mousemove", handleStickMove);
    }else{
        stickContainer.addEventListener("touchmove", handleStickMove);
    }
}
function handleStickEnd(){
  stickContainer.removeEventListener("mousemove", handleStickMove);
}
// ゲームパッドのスティックの移動イベント
function handleStickMove(event) {
  
  const stickContainer = event.target;
  const rect = stickContainer.getBoundingClientRect();

  // スティックの中心座標を計算
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  maxDistance = rect.width / 2;

  // タッチ座標またはマウス座標からスティックの位置を計算
  let clientX, clientY;
  if (event.touches) {
    clientX = event.touches[0].clientX;
    clientY = event.touches[0].clientY;
  } else {
    clientX = event.clientX;
    clientY = event.clientY;
  }
  const deltaX = clientX - centerX;
  const deltaY = clientY - centerY;

  // スティックの移動距離を制限
  const distance = Math.min(Math.sqrt(deltaX ** 2 + deltaY ** 2), maxDistance);

  // スティックの位置を更新
  stickX = deltaX / maxDistance;
  stickY = deltaY / maxDistance;

  // スティックの要素を移動
  stick.style.transform = `translate(${deltaX}px, ${deltaY}px)`;

  // x軸とy軸の値を表示
  console.log("x軸:", stickX.toFixed(2), "y軸:", stickY.toFixed(2));
}


// ゲームパッドのスティック要素にイベントリスナーを追加

handleStickReset()
if(checkDevice()){
    stickContainer.addEventListener("mousedown", handleStickStart);
    stickContainer.addEventListener("mouseup", handleStickEnd);
}else{
    stickContainer.addEventListener("touchstart", handleStickStart);
    stickContainer.addEventListener("touchend", handleStickEnd);
}