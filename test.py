import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert as trt

with tf.Session() as sess:
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], '/ml/data/example')

