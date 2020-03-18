import socket 
import numpy as np
import cv2
import os
import six.moves.urllib
import sys
'''
import tensorflow as tf
import zipfile'''
import time
'''from object_detection.utils import label_map_util
from collections import defaultdict'''
from io import StringIO
#from matplotlib import pyplot as plt
from PIL import Image
from queue import Queue
from _thread import *


enclosure_queue = Queue()
PATH_TO_CKPT = os.path.join('data','ssd_tensorrt','frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join('data','mscoco_label_map.pbtxt')
'''
NUM_CLASSES=90

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
'''
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

HOST = '165.246.41.45'
PORT = 31000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 
while True:
    message='1'
    start_time = time.time()
    client_socket.send(message.encode()) 
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    pic_time = time.time()
    data = np.frombuffer(stringData, dtype='uint8') 
    image_np=cv2.imdecode(data,1)
    print("Test Size: ", int(length)) 
    print("Test Runtime : %0.4f Sec"%(time.time() - start_time))
    print("Test Transmit 1 picture : %0.4f Sec"%(pic_time-start_time))
            #num = int(num_detections)
            #for i in range(num):
                #print(str(classes[0][i])+str(scores[0][i]))
            #cv2.imshow('Image',decimg)

client_socket.close()
