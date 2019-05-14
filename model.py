import tensorflow as tf
from tensorflow.keras import layers, optimizers, datasets, Sequential


batchsz = 128


def preprocess(x, y):
    """
    x is a simple image, not a batch
    """
    x = tf.cast(x, dtype=tf.float32) / 255.
    x = tf.reshape(x, [28, 28, 1])
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    return x,y

# 加载mnist数据集，第一次会从网上下载，保存在~/.keras/datasets/mnist.npz，
# 如果下载中断需要把这个文件删除重新下载，否则文件不完整会报错
(x, y), (x_val, y_val) = datasets.mnist.load_data()

print('datasets:', x.shape, y.shape, x.min(), x.max())

db = tf.data.Dataset.from_tensor_slices((x,y))
db = db.map(preprocess).shuffle(60000).batch(batchsz)
ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val))
ds_val = ds_val.map(preprocess).batch(batchsz)

conv_layers = [
    # unit 1
    layers.Conv2D(8, kernel_size=[3, 3], padding="same", activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2, 2], strides=2, padding='same'),

    # unit 2
    layers.Conv2D(16, kernel_size=[3, 3], padding="same", activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2, 2], strides=2, padding='same'),

    # unit 3
    layers.Conv2D(16, kernel_size=[3, 3], padding="same", activation=tf.nn.relu),
    layers.MaxPool2D(pool_size=[2, 2], strides=2, padding='same'),

    # 展开为向量
    tf.keras.layers.Flatten(),

    layers.Dense(512, activation=tf.nn.relu),
    # 输出层
    layers.Dense(10, activation=tf.nn.softmax),
]

net = Sequential(conv_layers)
# 输入数据为(x, 28, 28, 1)
net.build(input_shape=(None, 28, 28, 1))
net.summary()

net.compile(optimizer=optimizers.Adam(lr=0.001),
            loss=tf.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])
# 训练
net.fit(db, epochs=3, validation_data=ds_val, validation_freq=2)
# 评测
net.evaluate(ds_val)
# 保存模型
net.save('model/model.h5')
# 保存参数
net.save_weights('model/weights.ckpt')
