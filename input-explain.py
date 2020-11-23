from six.moves import urllib
import tensorflow as tf
import os
import gzip
import numpy
from .config import *

def data_type():
    #Return the type of the activations, weights, and placeholder variables.返回激活、权重和占位符变量的类型
    if FLAGS.use_fp16:
        return tf.float16
    else:
        return tf.float32


def maybe_download(filename):
    """Download the data from Yann's website, unless it's already here.从Yann的网站下载数据，除非它已经在这里。"""
    #查询是否有文件夹(WORK_DIRECTORY是一个文件夹)
    if not tf.gfile.Exists(WORK_DIRECTORY):
        #创建文件夹
        tf.gfile.MakeDirs(WORK_DIRECTORY)
    #连接文件夹和文件名（在这个文件夹里创建这个文件），filepath为这个连接后的路径
    filepath = os.path.join(WORK_DIRECTORY, filename)
    if not tf.gfile.Exists(filepath):
        #将来源URL表示的网络对象复制到本地文件，返回的filepath是可以找到对象的本体文件名，表示这个位置的返回值是不需要的变量
        filepath, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
        #获取文本操作句柄,即打开文件filepath，并视为f
        with tf.gfile.GFile(filepath) as f:
            #看f的大小
            size = f.size()
        print("Successfully downloaded", filename, size, "bytes.")
    return filepath


def extract_data(filename, num_images):
    '''
    读取下载文件的数据，转换成tensorflow识别的4维向量，并把数据归一化到[-0.5,0.5]
    Extract the images into a 4D tensor [image index, y, x, channels].Values are rescaled from [0, 255] down to [-0.5, 0.5].
    将图像提取为4d张量[图像索引，Y，X，通道]。值从[0，255]重新调整为[-0.5，0.5]
    '''
    print("Extracting", filename)
    #也就是bytestream=gzip.open(filename)，解压filename
    with gzip.open(filename) as bytestream:
        #返回从字符串中读取的字节，也就是读取bytestream的前16个字符
        bytestream.read(16)
        buf = bytestream.read(IMAGE_SIZE * IMAGE_SIZE * num_images * NUM_CHANNELS)
        #frombuffer将data以流的形式读入转化成ndarray对象，类型为uint8,ndarray 对象是用于存放同类型元素的多维数组。astype是再转化成float32的类型
        data = numpy.frombuffer(buf, dtype=numpy.uint8).astype(numpy.float32)
        data = (data - (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH
        #把data这个数据变成num_images个IMAGE_SIZE*IMAGE_SIZE矩阵的NUM_CHANNELS维数组的数据。
        data = data.reshape(num_images, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS)
        return data

#提取图像数据对应的标签
def extract_labels(filename, num_images):
    #Extract the labels into a vector of int64 label IDs.将标签提取到Int64标签ID的向量中。
    print("Extracting", filename)
    with gzip.open(filename) as bytestream:
        bytestream.read(8)
        buf = bytestream.read(1 * num_images)
        labels = numpy.frombuffer(buf, dtype=numpy.uint8).astype(numpy.int64)
    return labels


def fake_data(num_images):
    #Generate a fake dataset that matches the dimensions of MNIST.生成与mnist维度匹配的假数据集。
    data = numpy.ndarray(
        shape=(num_images, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS), dtype=numpy.float32
    )
    #返回来一个给定形状和类型的用0填充的数组
    labels = numpy.zeros(shape=(num_images,), dtype=numpy.int64)
    for image in xrange(num_images):
        label = image % 2
        data[image, :, :, 0] = label - 0.5
        labels[image] = label
    return data, labels
