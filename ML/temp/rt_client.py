import socket 
import numpy as np
import cv2
import os
import six.moves.urllib
import sys
import tensorflow as tf
import zipfile
import time
from object_detection.utils import label_map_util
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from queue import Queue
from _thread import *
from tensorflow.python.compiler.tensorrt import trt_convert as trt

enclosure_queue = Queue()
PATH_TO_LABELS = os.path.join('data','mscoco_label_map.pbtxt')

NUM_CLASSES=90
HOST = '165.246.41.45'
PORT = 31000

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def main():
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)



    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    client_socket.connect((HOST, PORT)) 
    message = '0'
    
    with tf.Session() as sess:
        print('model load')
        tf.compat.v1.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], '/ml/data/example')
        detection_graph = tf.get_default_graph()

        while True:
            overall_time = time.time()
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            client_socket.send(message.encode())
            length = recvall(client_socket,15)
            stringData = recvall(client_socket, int(length))
            data = np.frombuffer(stringData, dtype='uint8')
            image_np=cv2.imdecode(data,1)
            came_time = time.time()

            image_np_expanded = np.expand_dims(image_np, axis=0)
            (boxes, scores, classes, num_detections) = sess.run([boxes, scores, classes, num_detections], feed_dict={image_tensor: image_np_expanded})
            i = 0
            cls_name =  np.squeeze(classes.astype(np.int32))
            for i, v in enumerate(classes[0]):
                if float(scores[0][i]) > 0.4:
                    print("object : {}, score : {}".format(category_index[cls_name[i]]['name'],scores[0][i]))
            print("test Runtime : %0.5f sec"%(time.time()- came_time))
            print("Test Runtime : %0.5f sec"%(time.time() - overall_time))
            #num = int(num_detections)
            #for i in range(num):
                #print(str(classes[0][i])+str(scores[0][i]))
            #cv2.imshow('Image',decimg)


if __name__ == '__main__':
    main()
    
    client_socket.close()

