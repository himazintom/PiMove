from flask import Flask, render_template, request
import cv2
import numpy as np
from pybind import PictureModifier as pm
import base64
import re
import time
import logging

application = Flask(__name__, static_folder="./templates")

# ログの設定
application.logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
application.logger.addHandler(stream_handler)

@application.route('/')
def hello():
    return render_template('main.html')

@application.route('/deform', methods=['POST'])
def deform():
    application.logger.debug("画像変形処理を開始します")
    start_time = time.perf_counter()

    # Base64データをデコード
    image_data = request.form['image_data']
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    img_binary = base64.b64decode(image_data)
    nparr = np.frombuffer(img_binary, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        application.logger.error("画像のデコードに失敗しました")
        return "Error: 画像のデコードに失敗しました", 400

    # 画像のセットアップ
    count = pm.SetUpModifier(image, configure=0.3, move=np.array([0, 30]), frame=20)

    if count > 0:
        application.logger.debug(f"{count}箇所が検出されました")
        
        # GIF生成
        gif_data = pm.MakeGif()

        if gif_data is not None:
            # GIFをbase64エンコードして返す
            response = base64.b64encode(gif_data).decode('utf-8')
            application.logger.debug(f"処理完了: {time.perf_counter() - start_time}秒")
            return 'data:image/gif;base64,' + response
        else:
            application.logger.error("GIF生成に失敗しました")
            return "Error: GIF生成に失敗しました", 500
    else:
        application.logger.info("該当するオブジェクトが検出されませんでした")

        # 空のPNGを返す
        empty_image = np.zeros((1, 1, 3), np.uint8)  # 1x1ピクセルの黒画像
        _, buffer = cv2.imencode('.png', empty_image)
        response = base64.b64encode(buffer).decode('utf-8')
        return 'data:image/png;base64,' + response

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
