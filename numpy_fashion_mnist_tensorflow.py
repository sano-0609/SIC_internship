import tensorflow as tf
from tensorflow import keras
import keras
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

fashion_mnist = keras.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

class_name = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

fig = plt.figure(figsize=(9,9))
fig. subplots_adjust(left=0, right=1, bottom=0, top=0.5, hspace=0.05, wspace=0.05)

for i in range(81):
    ax = fig.add_subplot(9, 9, i + 1, xticks=[], yticks=[])
    ax.imshow(x_train[i].reshape((28, 28)), cmap='gray')
fig.savefig("fashion_mnist_data")

x_train = x_train / 255.0
x_test = x_test / 255.0

#層（モデル）の設定
model = keras.Sequential([keras.layers.Flatten(input_shape=(28, 28)), 
        keras.layers.Dense(128, activation = 'relu'), 
        keras.layers.Dense(10, activation = 'softmax')])
#モデルのコンパイル
model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

#モデルの訓練（訓練データ使用）
model.fit(x_train, y_train, batch_size=128, epochs=5)

#正解率の評価
test_loss, test_acc = model.evaluate(x_test, y_test, verbose = 2)
print('\nTest accuracy:', test_acc)

#画像の分類予測
predictions = model.predict(x_test)
for i in range(10):
    print("予想した数字（ラベル）：", np.argmax(predictions[i]))
    print("正解の数字（ラベル：）", y_test[i])
    print("予想した画像：", class_name[np.argmax(predictions[i])])
    print("正解の画像：", class_name[y_test[i]])