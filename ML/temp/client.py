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


enclosure_queue = Queue()
PATH_TO_CKPT = os.path.join('data','ssd_mobilenet_v3_small_coco_2019_08_14','frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join('data','mscoco_label_map.pbtxt')

NUM_CLASSES=90

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#detection_graph = tf.Graph()
#with detection_graph.as_default():
    #od_graph_def = tf.GraphDef()
    #with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        #serialized_graph = fid.read()
        #od_graph_def.ParseFromString(serialized_graph)
        #tf.import_graph_def(od_graph_def, name='')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
with tf.Session() as sess :
    tf.compat.v1.saved_model.loader.load( sess, "/ml/data/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb" )

HOST = '165.246.41.45'
PORT = 31000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 

with detection_graph.as_default():
        while True:
            message = '1'
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            client_socket.send(message.encode()) 
            length = recvall(client_socket,16)
            stringData = recvall(client_socket, int(length))
            data = np.frombuffer(stringData, dtype='uint8') 
            image_np=cv2.imdecode(data,1)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            start_vect = time.time()
            (boxes, scores, classes, num_detections) = sess.run([boxes, scores, classes, num_detections], feed_dict={image_tensor: image_np_expanded})

            print('test')
            i = 0
            cls_name =  np.squeeze(classes.astype(np.int32))
            for i, v in enumerate(classes[0]):
                if float(scores[0][i]) > 0.4:
                    print(scores[0][i])
                    print(category_index[cls_name[i]]['name'])
            print("Test Runtime : %0.5f Sec"%(time.time() - start_vect))
            #num = int(num_detections)
            #for i in range(num):
                #print(str(classes[0][i])+str(scores[0][i]))
            #cv2.imshow('Image',decimg)

client_socket.close()
