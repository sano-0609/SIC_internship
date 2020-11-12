import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

#データセットの確認
print("訓練データの画像セット", train_images)
print("訓練データのラベルセット", train_labels)
print("学習データの画像セット", test_images)
print("学習データのラベルセット", test_labels)

#データセットについての基礎情報の確認
print("配列の軸数（次元）：" + str(train_images.ndim))
print("テンソルの形状：" + str(train_images.shape))
print("テンソルのデータ型：" + str(train_images.dtype))

#訓練画像データのプロット（結果は画像保存）
fig = plt.figure()
digit = train_images[4]
plt.imshow(digit, cmap = plt.cm.binary)
fig.savefig("mnist_train")