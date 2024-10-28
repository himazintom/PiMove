from pybind import PictureModifier as pm
import imageio
import matplotlib.pyplot as plt
import os

image_path = "image.png"
image = imageio.imread(image_path)  # 画像を読み込んでNumPy配列に変換
pm.SetUpModifier(image)
pm.MakeGif()
images = pm.GetList()

output_folder = "output_images"  # 保存先フォルダの指定
os.makedirs(output_folder, exist_ok=True)  # フォルダが存在しない場合は作成

for idx, image in enumerate(images):  # インデックスを追加
    plt.imshow(image)
    plt.axis('off')  # 軸を非表示にする
    plt.savefig(os.path.join(output_folder, f'image_{idx}.png'))  # 画像を保存
    plt.close()  # プロットを閉じる