import os
os.add_dll_directory(r"C:\mingw64\bin")

from pybind import CPictureModifier as picm
import numpy as np
from pybind import PillowAndOpenCVChanger as poc
import torch
import math
import io
import matplotlib.pyplot as plt


imagePath = ""
image = np.array([1])

model = None
cripped_points = []
moveLength = np.array([0, 0])
frameVol = 0
pil_image = []
setupCheck = False

def SetUpModifier(_image, configure=0.3, move=np.array([0, 20]), frame=10):
    global image, imagePath, model, cripped_points, frameVol, timeDuration, pil_image, moveLength, setupCheck
    setupCheck = False
    image = _image

    # モデルが既に読み込まれていない場合のみロード
    if model is None:
        model = torch.hub.load(r'yolov5', 'custom', path=r"best.pt", source='local')

    frameVol = frame
    model.conf = max(0., min(configure, 1.))
    yresult = model(image)

    count = 0
    height, width = image.shape[:2]

    # バウンディングボックスを取得して画像をクリップ
    for idx, row in enumerate(yresult.pandas().xyxyn[0].itertuples()):
        xmin = math.floor(width * row.xmin)
        xmax = math.floor(width * row.xmax)
        ymin = math.floor(height * row.ymin)
        ymax = math.floor(height * row.ymax)

        # 偶数サイズに調整
        if (xmax - xmin) % 2 == 1:
            if xmax < width:
                xmax += 1
            else:
                xmin -= 1
        if (ymax - ymin) % 2 == 1:
            if ymax < height:
                ymax += 1
            else:
                ymin -= 1

        # 指定範囲を正方形に調整
        temp = (ymax - ymin) - (xmax - xmin)
        if temp > 0:
            ymax -= int(temp / 2)
            ymin += int(temp / 2)
        elif temp < 0:
            xmax -= int(-temp / 2)
            xmin += int(-temp / 2)

        # 境界を超えないように調整
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(width, xmax)
        ymax = min(height, ymax)

        cripped_points.append([xmin, xmax, ymin, ymax])
        count += 1

    print(f"{len(cripped_points)}個の該当部分があった")

    moveLength = move
    pil_image = []
    setupCheck = True
    return count

def MakeGif():
    a = image.copy()
    tempImages = []
    for k in range(frameVol):
        for j in cripped_points:
            iu = image.copy()[j[2]:j[3], j[0]:j[1]]
            # print(j[2],j[3], j[0],j[1])
            tempImages.append(picm.SquareCenterShake(iu, frameVol, k, moveLength))
        for i, j in enumerate(cripped_points):
            a[j[2]:j[3], j[0]:j[1]] = tempImages[i]
        pil_image.append(poc.cv2pil(a))  # NumPy配列をPillow Imageに変換せずに追加
    gif_data = io.BytesIO()
    # Pillowを使ってGIFを作成
    if pil_image:
        pil_image[0].save(gif_data, save_all=True, append_images=pil_image[1:], format='GIF', duration=100, loop=0)
    
    return gif_data.getvalue()

def GetList():
    return pil_image

