from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import RMSprop
import keras
import numpy as np
import matplotlib.pyplot as plt

#kerasを用いてデータを読み込む。xはデータ画像、yはデータのラベル
(x_train, y_train), (x_test, y_test) = mnist.load_data()


'''
#mnistデータの表示
fig = plt.figure(figsize=(9, 9))
fig. subplots_adjust(left=0, right=1, bottom=0, top=0.5, hspace=0.05, wspace=0.05)

for i in range(81):
    ax = fig.add_subplot(9, 9, i + 1, xticks=[], yticks=[])
    ax.imshow(x_train[i].reshape((28, 28)), cmap='gray')
fig.savefig("mnist_data")
'''
num_classes = 10 #分類したい数字の数は0~9なので10に設定
x_train = x_train.reshape(60000, 784)　#(60000, 28, 28)の形を変換
x_test = x_test.reshape(10000, 784)
#RGBの値(白→255, 黒→0)を利用して0~1の間に正規化
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

#ラベルをonehotベクトルに変換
y_train = y_train.astype('int32')
y_test = y_test.astype('int32')
y_train = keras.utils.np_utils.to_categorical(y_train, num_classes)
y_test = keras.utils.np_utils.to_categorical(y_test, num_classes)

print('x_train shape : ', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

model = Sequential() #レイヤー生成
model.add(Dense(512, activation='relu', input_shape=(784,))) # 入力のshape(形)は(512,784,)になる．
model.add(Dropout(0.2)) #過学習抑制のためニューロンをランダムに削除
model.add(Dense(512, activation='relu')) #２度目以降は入力のshapeをkerasが推定．
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax')) #softmaxは今回は分類問題なので，必要性は低い．

#訓練プロセスの設定
#RMSprop()は学習係数を過去の勾配を徐々に忘れる，"指数移動平均"を使う．
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])

batch_size = 128 #1回の学習あたりのデータ数
epochs = 20 #学習の回数
#historyにfittingの課程を保存．
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test))