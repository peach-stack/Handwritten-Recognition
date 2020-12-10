import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("input", one_hot=True)
from inference import inference
from loss import loss
from evaluation import accuracy_batch
from training import train
from save import save_model

if __name__ == "__main__":
    with tf.name_scope("inputs"):
        # 构建模型
        xs = tf.placeholder(tf.float32, [None, 784], name="x_input")
        ys = tf.placeholder(tf.float32, [None, 10], name="y_input")
        #模型的真实值
        keep_prob = tf.placeholder(tf.float32, name="dropout")
    # 最后一个参数是色深channel
    x_image = tf.reshape(xs, [-1, 28, 28, 1], name="image_input")
    prediction, logits = inference(x_image)
    predict_op = tf.argmax(prediction, 1, name="predict_op")
    # 预测值与真实值的交叉熵
    cross_entropy = loss(prediction, ys)
    # 使用梯度下降优化器最小交叉熵
    train_step = train(cross_entropy)

    train_prediction = tf.nn.softmax(prediction)  # 精确度

    sess = tf.Session()
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs/", sess.graph)
    sess.run(tf.initialize_all_variables())

    for i in range(1000):
        # 每次随机选取100个数据进行训练，即所谓的“随机梯度下降（Stochastic Gradient Descent，SGD）”
        batch_xs, batch_ys = mnist.train.next_batch(100)
        # 正式执行train_step，用feed_dict的数据取代placeholder
        sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5})
        if i % 50 == 0:
            #每训练50次后评估模型
            loss_value, accuracy_value = sess.run(
                [cross_entropy, train_prediction],
                feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5},
            )
            result = sess.run(
                merged, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5}
            )
            writer.add_summary(result, i)
            acc_v = accuracy_batch(accuracy_value, batch_ys)
            print("Loss", loss_value)
            print("Accuracy", acc_v)
    #保存模型
    save_model("export", x_image, predict_op, sess)

