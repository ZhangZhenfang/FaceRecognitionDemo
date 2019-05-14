import tensorflow as tf
import cv2
import numpy as np

# 加载模型
network = tf.keras.models.load_model('model/model.h5')
# 加载参数
network.load_weights('model/weights.ckpt')

# batchsz = 128
# def preprocess(x, y):
#     """
#     x is a simple image, not a batch
#     """
#     x = tf.cast(x, dtype=tf.float32) / 255.
#     x = tf.reshape(x, [None, 28, 28, 1])
#     y = tf.cast(y, dtype=tf.int32)
#     y = tf.one_hot(y, depth=10)
#     return x,y
# (x, y), (x_val, y_val) = datasets.mnist.load_data()

# x = tf.reshape(x, (60000, 28, 28, 1))
# print('datasets:', x.shape, y.shape, x.min(), x.max())
# for i in range(100):
#     cv2.imwrite("testimages/" + str(y_val[i]) + ".bmp", x_val[i])


# 读测试图片
images = np.empty((10, 28, 28))

for i in range(10):
    imread = cv2.imread("testimages/" + str(i) + ".bmp")
    imread = cv2.cvtColor(imread, cv2.COLOR_BGR2GRAY)
    imread = imread / 255.
    imread = cv2.resize(imread, (28, 28))
    images[i] = imread

images = tf.cast(images, dtype=tf.float32)
images = tf.reshape(images, (10, 28, 28, 1))

def predict(images):
    # 预测
    predict = network.predict(images)
    # 找到概率最大的位置
    argmax = tf.argmax(predict, axis=1)
    return argmax.numpy()
