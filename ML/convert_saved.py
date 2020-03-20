import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert as trt

print('trtgraphconvert')
converter = trt.TrtGraphConverter(
    input_saved_model_dir="/ml/data/ssd_mobilenet_v2_coco_2018_03_29/saved_model",
    nodes_blacklist=["detection_scores","detection_classes","detection_boxes","num_detections"],
    precision_mode="FP16")

print('convert')
converter.convert()
converter.save("/ml/data/example/")

'''
with tf.Session() as sess:
    # First deserialize your frozen graph:
    with tf.gfile.GFile("/ml/data/ssd_v2_fg.pb",'rb') as f:
        frozen_graph = tf.GraphDef()
        frozen_graph.ParseFromString(f.read())
    # Now you can create a TensorRT inference graph from your
    # frozen graph:
    converter = trt.TrtGraphConverter(
	    input_graph_def=frozen_graph,
	    nodes_blacklist=["detection_scores","detection_classes","detection_boxes","num_detections"],
            precision_mode="FP16")
    #output nodes
    print('convert')
    trt_graph = converter.convert()

    # Import the TensorRT graph into a new graph and run:
    print('finish')
    output_node = tf.import_graph_def(trt_graph,return_elements=["detection_scores","detection_classes","detection_boxes","num_detections"])
    '''
